import cv2
import os
import logging


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    # datefmt='%d-%b-%y %H:%M:%S'
                    )


def h_concat(imgs):
    imv = cv2.hconcat(imgs)
    return imv


def v_concat(imgs):
    imv = cv2.vconcat(imgs)
    return imv


def export_img_who(year):
    folder_path = os.path.join("info", year[0])
    img_path = os.path.join(folder_path, "who_corr.png")
    img1 = cv2.imread(img_path)
    folder_path = os.path.join("info", year[1])
    img_path = os.path.join(folder_path, "who_corr.png")
    img2 = cv2.imread(img_path)
    img_new = h_concat([img1, img2])
    out_path = os.path.join("info", "who_corr_plot.jpg")
    cv2.imwrite(out_path, img_new)
    logging.info(f"Image saved in {out_path}")


def export_img(year):
    folder_path = os.path.join("info", year)
    ver_img_list = []
    col_1 = ['affect', 'appreciation', 'judgement']
    col_2 = ['New_cases', 'New_deaths']
    for i in col_2:
        hor_img_list = []
        for j in col_1:
            file_name = f"{j}_{i}.png"
            file_path = os.path.join(folder_path, file_name)
            hor_img_list.append(cv2.imread(file_path))
        ver_img_list.append(h_concat(hor_img_list))
    concat_img = v_concat(ver_img_list)
    out_path = os.path.join("info", f"{year}_corr_plot.jpg")
    cv2.imwrite(out_path, concat_img)
    logging.info(f"Image saved in {out_path}")


def main():
    year = ["2020", "2021"]
    export_img_who(year)
    for i in year:
        export_img(i)


if __name__ == "__main__":
    main()
