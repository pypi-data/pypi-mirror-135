import cv2
import numpy as np
import matplotlib.pyplot as plt        
from mpl_toolkits.mplot3d import Axes3D  
def opt_trace(video_path,maxC,qualitylv,minDist,xrange,yrange):
    try:
        cap = cv2.VideoCapture(video_path)

        ft_params = dict(maxCorners=maxC,  
                        qualityLevel=qualitylv,  
                        minDistance=minDist,  
                        blockSize=7) 

        lk_params = dict(winSize=(15, 15),  
                        maxLevel=2,  
                        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        ret, frame = cap.read()
        gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        ft1 = cv2.goodFeaturesToTrack(
            gray1, mask=None, **ft_params)

        li = []
        if not xrange == "none" and not yrange == "none":
            for i in list(range(0,len(ft1[:,0]))):
                ftt = list(ft1[:,0][i])
                if xrange[0] < ftt[0] < xrange[1] and yrange[0] < ftt[1] < yrange[1]:
                    li.append([ftt])
            ft1 = np.array(li)
        elif not xrange == "none" and yrange == "none":
            for i in list(range(0,len(ft1[:,0]))):
                ftt = list(ft1[:,0][i])
                if xrange[0] < ftt[0] < xrange[1]:
                    li.append([ftt])
            ft1 = np.array(li)
        elif xrange == "none" and not yrange == "none":
            for i in list(range(0,len(ft1[:,0]))):
                ftt = list(ft1[:,0][i])
                if yrange[0] < ftt[1] < yrange[1]:
                    li.append([ftt])
            ft1 = np.array(li)

        coord_list = []
        for i in range(len(ft1)):
            coord_list.append({"x":[],"y":[]})


        mask = np.zeros_like(frame)

        def col_rgb(co):
            co_ = co/255
            return co_

        color_list = [[0,0,255],[0,255,0],[255,0,0],[255,0,255],[255,255,0],[0,255,255],[255,111,111],[111,255,111],[111,111,255],[111,111,111]]
        color_box = []
        for i in range(len(ft1)):
            color_ = reversed(list(map(col_rgb,color_list[i])))
            color_box.append(list(color_))

        while(cap.isOpened()):
            try:
                ret, frame = cap.read()
                gray2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                ft2, status, err = cv2.calcOpticalFlowPyrLK(
                    gray1, gray2, ft1, None, **lk_params)

                good1 = ft1[status == 1]
                good2 = ft2[status == 1] 
                count_ = 0

                for i, (pt2, pt1) in enumerate(zip(good2, good1)):
                    x1, y1 = pt1.ravel()
                    x2, y2 = pt2.ravel()
                    coord_list[count_]["x"].append(int(x2))
                    coord_list[count_]["y"].append(int(y2))

                    mask = cv2.line(mask, (int(x2), int(y2)), (int(x1), int(y1)),color_list[count_], 2)
                    frame = cv2.circle(frame, (int(x2), int(y2)), 5,  color_list[count_], -1)
                    count_ += 1

                img = cv2.add(frame, mask)

                cv2.imshow('mask', img)       

                gray1 = gray2.copy()
                ft1 = good2.reshape(-1, 1, 2)

                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break
            except:
                break

        H = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        def adjus_high(high):
            re = int(H) - high
            return re

        fig = plt.figure()
        ax = Axes3D(fig)
        count = 0
        for i in coord_list:
            xx = i["x"]
            yy_ = i["y"]
            yy = list(map(adjus_high, yy_))

            zz = list(reversed(range(1,len(xx)+1)))
            ax.plot(xx, yy, zz,color=color_box[count])
            count += 1
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('time')
        plt.show()

        cv2.destroyAllWindows()
        cap.release()
    except:
        print("Please check the arguments.")