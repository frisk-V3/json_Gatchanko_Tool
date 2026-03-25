import json
import glob
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

class JsonMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON配列マージツール（本気版）")
        self.root.geometry("600x450")

        self.label = tk.Label(root, text="フォルダ内のJSONを1つの配列にまとめます", pady=10)
        self.label.pack()

        self.select_btn = tk.Button(root, text="フォルダを選択", command=self.select_folder)
        self.select_btn.pack(pady=5)

        self.run_btn = tk.Button(root, text="配列で結合開始！", command=self.merge_json_array,
                                 bg="#0078D7", fg="white", state="disabled")
        self.run_btn.pack(pady=10)

        self.log_area = scrolledtext.ScrolledText(root, height=15, width=70)
        self.log_area.pack(padx=10, pady=10)

        self.selected_dir = ""

    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)

    def select_folder(self):
        directory = filedialog.askdirectory()
        if directory:
            self.selected_dir = directory
            self.log(f"【選択】: {directory}")
            self.run_btn.config(state="normal")

    def merge_json_array(self):
        output_file_name = "merged_array.json"
        output_path = os.path.join(self.selected_dir, output_file_name)

        search_path = os.path.join(self.selected_dir, "*.json")
        files = [f for f in glob.glob(search_path) if os.path.basename(f) != output_file_name]

        if not files:
            messagebox.showwarning("警告", "JSONファイルがありません。")
            return

        self.log("--- 処理開始 ---")
        result = []
        count = 0

        try:
            for file_path in sorted(files):
                with open(file_path, 'r', encoding='utf-8') as infile:
                    try:
                        data = json.load(infile)

                        # リスト → 展開
                        if isinstance(data, list):
                            result.extend(data)
                            count += len(data)

                        # 辞書 → そのまま追加
                        elif isinstance(data, dict):
                            result.append(data)
                            count += 1

                        else:
                            self.log(f"⚠ 形式不明: {os.path.basename(file_path)}（list でも dict でもない）")
                            continue

                        self.log(f"読み込み成功: {os.path.basename(file_path)}")

                    except Exception as e:
                        self.log(f"読み込み失敗: {os.path.basename(file_path)} ({e})")

            # ★ 最後に1つの配列として書き込む
            with open(output_path, 'w', encoding='utf-8') as outfile:
                json.dump(result, outfile, ensure_ascii=False, indent=2)

            self.log(f"\n完了！ 合計 {count} 件のデータを配列として保存しました。")
            self.log(f"保存先: {output_path}")
            messagebox.showinfo("成功", f"{count} 件のデータを結合しました。")

        except Exception as e:
            messagebox.showerror("エラー", f"ファイル保存中にエラーが発生しました: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = JsonMergerApp(root)
    root.mainloop()
