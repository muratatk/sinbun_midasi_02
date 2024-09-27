import tkinter as tk
from tkinter import messagebox, Listbox
from PIL import Image, ImageTk
import os
import time

# 画像ディレクトリのパス
image_directory = 'C:\\Users\\knk01040\\Desktop\\png_新聞記事_2024_08'
output_directory = 'C:\\Users\\knk01040\\Desktop\\抽出_png'

# メインウィンドウの作成
root = tk.Tk()
root.title("画像表示ツール")
root.geometry("800x600")

# Canvasの作成
canvas = tk.Canvas(root, bg='white')
canvas.pack(fill=tk.BOTH, expand=True)

# 画像の変数を保持
image_tk = None
image = None
rectangles = []
rect_coords = []


# 画像を読み込んでCanvasに表示する関数
def load_image():
    global image_tk, image

    # リストボックスで選択されたファイル名を取得
    selected_file = file_listbox.get(file_listbox.curselection())

    # 画像パスの作成
    image_path = os.path.join(image_directory, selected_file)

    # ファイルの存在確認
    if not os.path.isfile(image_path):
        messagebox.showerror("エラー", f"ファイルが見つかりません: {image_path}")
        return

    # 画像の読み込み
    try:
        image = Image.open(image_path)
        image_tk = ImageTk.PhotoImage(image)

        # Canvasをクリアして新しい画像を表示
        canvas.delete("all")
        canvas.create_image(0, 0, anchor='nw', image=image_tk)
        canvas.config(scrollregion=canvas.bbox(tk.ALL))  # スクロール領域の設定
    except Exception as e:
        messagebox.showerror("エラー", f"画像を読み込めません: {e}")


# 指定ディレクトリ内のファイル名一覧を取得
def list_files():
    try:
        files = os.listdir(image_directory)
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        for file in image_files:
            file_listbox.insert(tk.END, file)
    except Exception as e:
        messagebox.showerror("エラー", f"ファイルをリストできません: {e}")


# マウスのクリックで長方形の描画を開始
def on_button_press(event):
    start_x = canvas.canvasx(event.x)
    start_y = canvas.canvasy(event.y)
    rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red', width=2)
    rectangles.append(rect)
    rect_coords.append((start_x, start_y, start_x, start_y))


# マウスのドラッグで長方形を拡大
def on_drag(event):
    x1, y1, _, _ = rect_coords[-1]
    x2 = canvas.canvasx(event.x)
    y2 = canvas.canvasy(event.y)
    canvas.coords(rectangles[-1], x1, y1, x2, y2)
    rect_coords[-1] = (x1, y1, x2, y2)


# 完了ボタンを押したときに赤枠内の領域を保存
def save_cropped_images():
    global image
    for i, (x1, y1, x2, y2) in enumerate(rect_coords):
        # 赤枠の座標で画像を切り出し
        cropped_image = image.crop((int(x1), int(y1), int(x2), int(y2)))
        timestamp = int(time.time())
        output_path = os.path.join(output_directory, f"extracted_{timestamp}_{i}.png")
        cropped_image.save(output_path)
        print(f"画像が保存されました: {output_path}")
    messagebox.showinfo("完了", "選択領域の画像が保存されました。")


# フォームの作成
form_frame = tk.Frame(root)
form_frame.pack(pady=10)

# ファイル名一覧のリストボックス
file_listbox = Listbox(form_frame, width=50, height=10)
file_listbox.grid(row=0, column=0, padx=10, pady=10)

# 表示ボタン
load_button = tk.Button(form_frame, text="表示", command=load_image)
load_button.grid(row=0, column=1, padx=10)

# 完了ボタン
save_button = tk.Button(form_frame, text="完了", command=save_cropped_images)
save_button.grid(row=1, column=0, columnspan=2, pady=10)

# ファイル一覧の読み込み
list_files()

# Canvasのバインド
canvas.bind("<ButtonPress-1>", on_button_press)
canvas.bind("<B1-Motion>", on_drag)

root.mainloop()
