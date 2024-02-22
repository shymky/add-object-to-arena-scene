import time
from argparse import ArgumentParser
from watchdog.events import FileSystemEventHandler
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
import shutil

import os
from argparse import ArgumentParser

from arena import *
import asyncio
import os
import random

on_created = False
file_name = None

# ユーザー名を取得
global username
username = os.getlogin()

def add_glb(scene, file_name):

    randx = random.randint(0,10)
    randz = random.randint(0,10)
    obj = GLTF(object_id="AirDroppedObject"+str(random.randrange(10**11,10**12)),
        position=(randx,0, randz),
        scale=(1, 1, 1),
        url=f"store/{file_name}",
        persist=False)
    scene.add_object(obj)
    print('add Object')



class MyWatchHandler(PatternMatchingEventHandler):
    """監視ハンドラ"""
    def __init__(self,patterns=['*.glb']):
    # def __init__(self,patterns=['*.yaml']):
        """コンストラクタ"""
        super().__init__(patterns)
        self.known_file = []

    def on_any_event(self, event):
        """全イベント検知

        Args:
            event: 検知イベント
        """
        # print(f'[on_any_event] {event}')
        pass

    def on_moved(self, event):
        """moved検知関数

        Args:
            event: イベント
        """
        #print(f"[on_moved] {event}")

    def on_created(self, event):
        airdropped_file_path = event.src_path

        #arenaのstoreフォルダに3dオブジェクトを追加します
        arena_store_path = f'/Users/{username}/arena-tutorial/arena-services-docker/store'
        s = airdropped_file_path.split("/")
        global file_name
        for a in s:
            if a.endswith('.glb'):
                file_name = a
        print(file_name)
        if airdropped_file_path not in self.known_file and os.path.exists(airdropped_file_path):  # ソースファイルが存在するか確認(AirDrop)ではなぜかcreateが３回起動するのでそれへの対処法
            print(f"{airdropped_file_path} was created.")

            #AirDropではファイルの中身よりも先に空ファイルが作成されるので、ちゃんと中身が存在するかの確認
            while os.path.getsize(airdropped_file_path)==0:
                time.sleep(10)
            shutil.copy(airdropped_file_path,arena_store_path)
            global on_created
            while os.path.getsize(arena_store_path)==0:
                time.sleep(1)
            time.sleep(3)
            on_created = True
            self.known_file.append(airdropped_file_path)
            print(f"Copied to arena!: {airdropped_file_path} -> {arena_store_path}")


def monitor(path,scene):
    """監視実行関数
    Args:
        path: 監視対象パス
    """

    global on_created
    event_handler = MyWatchHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            if on_created:
                on_created = False
                add_glb(scene,file_name)#sceneにファイルを追加する文
                print("")
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def main():
    """メイン関数"""
    # ===== ArgumentParserの設定
    parser = ArgumentParser(description="Monitoring Tool")
    # 引数の処理
    parser.add_argument("-p", "--path", action="store", dest="path", help="監視対象パス")
    # コマンドライン引数のパース
    args = parser.parse_args()
    # 引数の取得
    path = args.path
    # pathの指定がない場合はデフォルトのダウンロードディレクトリに設定
    if path is None:
        # ユーザー名を取得
        path = f"/Users/{username}/Downloads"
    scene = Scene(host="localhost", scene="example")  # シーンを指定
    monitor(path, scene)

if __name__ == "__main__":
    main()
