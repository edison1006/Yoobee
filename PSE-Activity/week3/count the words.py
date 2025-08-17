import pandas as pd

def count_words(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    df = pd.DataFrame(lines, columns=["line"])
    return df["line"].astype(str).str.split().explode().size

def main():
    demo_path = "/Users/zhangxiaoyu/Desktop/Yoobee/PSE/week3/Activity/eBook.txt"
    total_words = count_words(demo_path)
    print(f"Total words: {total_words}")

if __name__ == "__main__":
    main()
