import os
import cv2
import numpy as np

def compare_color_histograms(hist1, hist2):
    # Вычисляем гистограммы совпадений для цветов
    match_percent = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return match_percent


def video_comparison(path1, path2):
    video1 = cv2.VideoCapture(path1)
    video2 = cv2.VideoCapture(path2)
    ret1, frame1 = video1.read()
    ret2, frame2 = video2.read()
    if ret1 and ret2:
        # Преобразуем кадры в пространство цветов RGB
        frame1_rgb = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        frame2_rgb = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        # Вычисляем гистограммы цветов для каждого кадра
        hist1 = cv2.calcHist([frame1_rgb], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist2 = cv2.calcHist([frame2_rgb], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        # Нормализуем гистограммы
        cv2.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
        cv2.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
        # Сравниваем гистограммы цветов
        match_percent = compare_color_histograms(hist1, hist2)
        # print("Процент совпадения цветов между первыми кадрами двух видео:", match_percent * 100, "%")
        # Освобождаем ресурсы
        video1.release()
        video2.release()
        return match_percent * 100
    else:
        # print("Не удалось загрузить кадры из одного или обоих видео")
        return None


def main(path_to_dir):
    root = rf'{os.path.dirname(path_to_dir)}/result'
    # Проходимся по всем папкам
    for cur_dir in os.listdir(root):
        cur_dir = rf"{root}\{cur_dir}"
        # Находим одинаковые видео по хронометражу
        videos = os.listdir(cur_dir)
        video_by_chrono = {}
        for path in videos:
            video = cv2.VideoCapture(rf"{cur_dir}\{path}")
            total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = int(video.get(cv2.CAP_PROP_FPS))
            duration_seconds = total_frames // fps
            if duration_seconds not in video_by_chrono:
                video_by_chrono[duration_seconds] = [path]
            else:
                video_by_chrono[duration_seconds].append(path)
        # Находим одинаковые видео по контексту
        same_videos_dict = dict()
        for chrono, videos in video_by_chrono.items():
            same_videos_dict[chrono] = dict()
            while videos:
                same_videos_dict[chrono][videos[0]] = set()
                index = 1
                while index < len(videos):
                    match_percent = video_comparison(rf"{cur_dir}\{videos[0]}", rf"{cur_dir}\{videos[index]}")
                    # Если плохо работает можно изменить процент сходства
                    if 99 <= match_percent <= 100:
                        same_videos_dict[chrono][videos[0]].add(videos[index])
                        videos.pop(index)
                    else:
                        index += 1
                videos.pop(0)
        # Выбираем из одинаковых по контексту и хронометражу самые хорошие по качеству (самые тяжелые)
        for videos in same_videos_dict.values():
            for video, same_video in videos.items():
                if same_video:
                    same_video.add(video)
                    best_video = max([(os.path.getsize(rf'{cur_dir}\{path}'), path) for path in same_video])[1]
                    [os.remove(rf'{cur_dir}\{path}') for path in same_video if path != best_video]

