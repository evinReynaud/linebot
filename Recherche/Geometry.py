
#Calculate line from the coords
def get_Line(x1,y1,x2,y2):
    a = float(y2-y1) / (x2-x1) if x2 != x1 else 0
    b = y1 - a*x1 #Equation de droite
    return a, b

# w for width, x for the x coord of a point
def get_shift(x,w):
    hw = w/2
    return 100 *(x-hw)/hw

def get_Angle(p1,p2,w,h):

    #Correct p1 and p2
    px1 = p1[0] - w/2
    px2 = p2[0] - w/2
    py1 = h - p1[0]
    py2 = h - p2[0]

    



# Get the box vector, box is the biggest contour detected
def calc_box_vector(box):
    v_side = calc_line_length(box[0], box[3])
    h_side = calc_line_length(box[0], box[1])
    idx = [0, 1, 2, 3]
    if v_side < h_side:
        idx = [0, 3, 1, 2]
    return ((box[idx[0]][0] + box[idx[1]][0]) / 2, 
            (box[idx[0]][1] + box[idx[1]][1]) / 2), 
            ((box[idx[2]][0] + box[idx[3]][0]) / 2, 
            (box[idx[2]][1]  +box[idx[3]][1]) / 2)