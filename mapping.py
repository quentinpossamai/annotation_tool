import cv2
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pickle
import datetime

matplotlib.use('TKAgg')

FRAME_NUM = 0
INVERT = False
POINT_NUMBER = 1  # 0, 1, 2, 3


def label_data(video_path: str, labels_path: str):
    """
    Label the frame of a video file with using matplotlib and cursor position.

    param video_path: The path to load the video from.
    param label_path: The path to save the label from.
    :return:
    """
    global FRAME_NUM
    video = cv2.VideoCapture(video_path)
    img = []
    is_reading, frame = video.read()
    height, width, _, = frame.shape
    while is_reading:
        # read video is in bgr.
        img.append(np.array(frame[:, :, ::-1]))
        is_reading, frame = video.read()
    img = np.stack(img)
    _, height, width, _ = img.shape
    try:
        msg = f'Previous labels found at: {labels_path}'
        labels = pickle.load(open(f'{labels_path}', 'rb'))
    except FileNotFoundError:
        msg = f'No previous label found.'
        labels = {0: {}, 1: {}, 2: {}, 3: {}}
    print(msg)

    FRAME_NUM = 0
    # fig, ax = plt.subplots(1, 1, figsize=(2.5 * 6.4, 2 * 4.8))
    fig, ax = plt.subplots(1, 1, figsize=(1.2 * width / 100, 1.2 * height / 100))
    ax.set_title(f'Frame: {FRAME_NUM}')
    img_obj = ax.imshow(img[FRAME_NUM])
    ax.grid(False)
    scatter_obj = {0: ax.scatter(width / 2, height / 2, c='r', alpha=0),
                   1: ax.scatter(width / 2, height / 2, c='r', alpha=0),
                   2: ax.scatter(width / 2, height / 2, c='r', alpha=0),
                   3: ax.scatter(width / 2, height / 2, c='r', alpha=0)}
    for i in range(4):
        if 0 in labels[i]:
            scatter_obj[i].set_alpha(1)
            value = labels[i][0]
            scatter_obj[i].set_offsets(value[0])
            scatter_obj[i].set_color('g' if value[1] else 'r')

    def display_other_frame(increment):
        global FRAME_NUM
        global INVERT
        FRAME_NUM = FRAME_NUM + increment
        if INVERT:
            img_obj.set_data(255 - img[FRAME_NUM])
        else:
            img_obj.set_data(img[FRAME_NUM])
        for i_ind in range(4):
            if FRAME_NUM in labels[i_ind]:
                val = labels[i_ind][FRAME_NUM]
                scatter_obj[i_ind].set_alpha(1)
                if val[1]:  # keyframe
                    scatter_obj[i_ind].set_offsets(labels[i_ind][FRAME_NUM][0])
                    scatter_obj[i_ind].set_color('g')
                else:
                    scatter_obj[i_ind].set_color('r')
                    scatter_obj[i_ind].set_offsets(labels[i_ind][FRAME_NUM][0])
            else:
                scatter_obj[i_ind].set_alpha(0)
        ax.set_title(f'Frame: {FRAME_NUM}')
        fig.canvas.draw()

    # If the labelling is done with the click.
    # def on_click(event):
    #     if event.button.name == 'LEFT':
    #         label[FRAME_NUM] = np.array([np.round(event.xdata), np.round(event.ydata)])
    #         display_other_frame(1)

    def on_key(event):
        global INVERT
        if event.key == 'e':
            labels[POINT_NUMBER][FRAME_NUM] = (np.array([np.round(event.xdata), np.round(event.ydata)]), False)  # not a key frame
            display_other_frame(1)
        if event.key == ' ':
            labels[POINT_NUMBER][FRAME_NUM] = (np.array([np.round(event.xdata), np.round(event.ydata)]), True)  # a key frame
            display_other_frame(1)
        if event.key == '1':
            display_other_frame(-1)
        if event.key == '2':
            display_other_frame(1)
        if event.key == '3':
            display_other_frame(-10)
        if event.key == '4':
            display_other_frame(10)
        if event.key == '5':
            display_other_frame(-100)
        if event.key == '6':
            display_other_frame(100)
        if event.key == 'r':
            INVERT = not INVERT
            display_other_frame(0)
        if event.key == 'd':
            del labels[POINT_NUMBER][FRAME_NUM]
            display_other_frame(0)
        if event.key == 'w':
            h = datetime.datetime.now()
            print(f'{h.ctime()}: Saving at: {labels_path}')
            pickle.dump(labels, open(f'{labels_path}', 'wb'))

    # fig.canvas.mpl_connect('button_press_event', on_click)
    fig.canvas.mpl_connect('key_press_event', on_key)
    plt.show()


def main():
    label_data(video_path=f'path_to_video.mkv', labels_path=path_to_labels.pkl)
    
if __name__ == '__main__':
    main()
