import xml.etree.ElementTree as ET
import math
import glob
import os
import cv2

def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    image_size = root.find('size')
    width = int(image_size.find('width').text)
    height = int(image_size.find('height').text)
    
    annotations = []
    
    for obj in root.findall('object'):
        class_name = obj.find('name').text
        bbox = obj.find('bndbox')
        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)
        
        annotations.append({
            'class': class_name,
            'xmin': xmin,
            'xmax': xmax,
            'ymin': ymin,
            'ymax': ymax,
        })
    
    return width, height, annotations


def find_class_index(class_name):
    if class_name == "Radar":
        return 0
    elif class_name == "LTE":
        return 1
    elif class_name == "DSSS":
        return 2
    elif class_name == "5G":
        return 3
    
def find_center(min, max, size):
    return ((min+max)/2)/size


def make_yolo_txt(width, height, annotations):
    
    split_width = math.ceil(width/2)
    split_height = height

    annotation1 = []
    annotation2 = []

    for annotation in annotations:
        class_name = annotation['class']
        xmin = annotation['xmin']
        xmax = annotation['xmax']
        ymin = annotation['ymin']
        ymax = annotation['ymax']

        class_index = find_class_index(class_name)   
        y_center = round(find_center(ymin, ymax, split_height), 6)
        bbox_height = round((ymax-ymin)/split_height, 6)

        if xmin<split_width and xmax<split_width:
            x_center = round(find_center(xmin, xmax, split_width), 6)
            bbox_width = round((xmax-xmin)/split_width, 6)
            annotation1.append({
                'class': class_index,
                'x_center': x_center,
                'y_center': y_center,
                'bbox_width': bbox_width,
                'bbox_height': bbox_height
            })

        if xmin<split_width and xmax>split_width:
            x_center = round(find_center(xmin, split_width, split_width), 6)
            bbox_width = round((split_width-xmin)/split_width, 6)
            annotation1.append({
                'class': class_index,
                'x_center': x_center,
                'y_center': y_center,
                'bbox_width': bbox_width,
                'bbox_height': bbox_height
            })
            x_center = round(find_center(0, xmax-split_width, split_width), 6)
            bbox_width = round((xmax-split_width)/split_width, 6)
            annotation2.append({
                'class': class_index,
                'x_center': x_center,
                'y_center': y_center,
                'bbox_width': bbox_width,
                'bbox_height': bbox_height
            })

        if xmin>=split_width and xmax>=split_width:
            x_center = round(find_center(xmin-split_width, xmax-split_width, split_width), 6)
            bbox_width = round((xmax-xmin)/split_width, 6)
            annotation2.append({
                'class': class_index,
                'x_center': x_center,
                'y_center': y_center,
                'bbox_width': bbox_width,
                'bbox_height': bbox_height
            })

    return annotation1, annotation2
        
        


def write_annotations_to_file(annotations, output_file):
    i = 0
    with open(output_file, 'w') as f:
        for annotation in annotations:
            line = ' '.join([str(value) for value in annotation.values()])
            if i==0:
                f.write(line)
                i = i+1
            else:
                f.write('\n' + line)


def split_images():
    files = glob.glob(os.path.join(input_img_dir, '*.jpg'))
    for img in files:
        basename = os.path.basename(img)
        filename = os.path.splitext(basename)[0]
        image = cv2.imread(img)
        height, width, channels = image.shape
        half_width = math.ceil(width/2)

        split1 = image[:, :half_width]
        split2 = image[:, half_width:]
        
        cv2.imwrite(os.path.join(output_img_dir, f"{filename}_1.jpg"), split1)
        cv2.imwrite(os.path.join(output_img_dir, f"{filename}_2.jpg"), split2)
        
        print(f"Saved {filename}_1, {filename}_2")


input_label_dir = "annotations"     #input labels directory
output_label_dir = "frequency_split_labels"     #output labels directory
input_img_dir = "input_images"      #input images directory
output_img_dir = "frequency_split_img"      #output images directory

os.mkdir(output_label_dir)
os.mkdir(output_img_dir)

split_images()

files = glob.glob(os.path.join(input_label_dir, '*.xml'))
for file in files:
    basename = os.path.basename(file)
    filename = os.path.splitext(basename)[0]

    width, height, annotations = parse_xml(file)
    annotation1, annotation2 = make_yolo_txt(width, height, annotations)
    if annotation1:
        write_annotations_to_file(annotation1, os.path.join(output_label_dir, f"{filename}_1.txt"))
    else:
        print(f"No bounding box for {filename}_1")
        os.remove(os.path.join(output_img_dir, f'{filename}_1.jpg'))
    if annotation2:
        write_annotations_to_file(annotation2, os.path.join(output_label_dir, f"{filename}_2.txt"))
    else:
        print(f"No bounding box for {filename}_2")
        os.remove(os.path.join(output_img_dir, f'{filename}_2.jpg'))

