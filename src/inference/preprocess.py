import os
import cv2
import random
import shutil

# CONFIG
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
CATEGORIES = ["empty", "half", "full", "overflow"]
IMG_SIZE = 224
TRAIN_SPLIT = 0.8
RANDOM_SEED = 42

random.seed(RANDOM_SEED)

def create_dirs():
    for split in ["train", "test"]:
        for category in CATEGORIES:
            path = os.path.join(PROCESSED_DIR, split, category)
            os.makedirs(path, exist_ok=True)

def process_and_split():
    for category in CATEGORIES:
        category_path = os.path.join(RAW_DIR, category)
        images = os.listdir(category_path)
        images = [img for img in images if img.lower().endswith(('.jpg', '.png', '.jpeg'))]

        random.shuffle(images)
        split_idx = int(len(images) * TRAIN_SPLIT)

        train_imgs = images[:split_idx]
        test_imgs = images[split_idx:]

        for split, img_list in zip(["train", "test"], [train_imgs, test_imgs]):
            for img_name in img_list:
                src_path = os.path.join(category_path, img_name)
                dst_path = os.path.join(PROCESSED_DIR, split, category, img_name)

                img = cv2.imread(src_path)
                if img is None:
                    print(f"⚠️ Skipping corrupted image: {src_path}")
                    continue

                img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
                cv2.imwrite(dst_path, img)

        print(f"✅ {category}: {len(train_imgs)} train | {len(test_imgs)} test")

if __name__ == "__main__":
    # Clean old processed data
    if os.path.exists(PROCESSED_DIR):
        shutil.rmtree(PROCESSED_DIR)

    create_dirs()
    process_and_split()

    print("\n🎯 Dataset preprocessing completed successfully")
