import xml.etree.ElementTree as ET
import os

directory_path = "..\\product_data\\product_data\\reviews"
testDataSet_path = "..\\product_data\\product_data\\reviews\\reviews_0001_24122_to_98772.xml"

def foldername(path):
    for subdir, dirs, files in os.walk(path):
        for file in files:
            print(os.path.join(subdir, file))


def xml_preprocess(path):
    skuDict = dict()
    for subdir, dirs, files in os.walk(path):
        for filepath in files:
            # print(os.path.join(subdir, file))
            file = open(os.path.join(subdir, filepath), encoding='utf-8')
            tree = ET.parse(file)
            root = tree.getroot()

            for page in list(root):
                sku = page.find('sku').text
                rating = page.find('rating').text
                if sku not in skuDict:
                    skuDict[sku] = [float(rating), 1]
                else:
                    skuDict[sku][0] += float(rating)
                    skuDict[sku][1] += 1
                # print('sku: %s; rating: %s' % (sku, rating))
    return skuDict

def xml_preprocesswname(path):
    skuDict = dict()
    for subdir, dirs, files in os.walk(path):
        for filepath in files:
            file = open(os.path.join(subdir, filepath), encoding='utf-8')
            tree = ET.parse(file)
            root = tree.getroot()

            for page in list(root):
                name = page.find('reviewer').find('name').text
                sku = page.find('sku').text
                rating = page.find('rating').text
                print('name: %s; sku: %s; rating: %s' % (name, sku, rating))
    return skuDict

def avgReviewRate(dict):
    for avgrate in dict:
        if dict[avgrate][0] != 0 and dict[avgrate][1] != 0:
            avg = float(dict[avgrate][0])/float(dict[avgrate][1])
            dict[avgrate][0] = avg
        else:
            avg = 0
            dict[avgrate][0] = avg

    return dict
print(xml_preprocesswname(directory_path))
# print(avgReviewRate(xml_preprocess(directory_path)))
# print(xml_preprocess(directory_path))
# print(foldername(directory_path))