import calendar
import datetime
import exifread
import os
import shutil

foldersAndFiles = {}
DIRECTORY = "."
CWD = os.getcwd()
invalidDir = "Manual_Review"

def parseMonth(month):
    return calendar.month_abbr[int(month)]

def parseDate(date_taken):
    date_taken_array = date_taken.split(":")
    year = date_taken_array[0]
    month = date_taken_array[1]
    month = parseMonth(month)
    dateStamp = year+"-"+month
    return dateStamp

def addData(dateStamp, File, dict):
    if dateStamp in foldersAndFiles.keys():
        dict[dateStamp].append(File)
    else:
        foldersAndFiles[dateStamp] = [File]

def main():
    try:
        os.makedirs(invalidDir)
    except Exception as e:
        if "Cannot create a file when that file already exists" in str(e):
                print("'"+invalidDir+"' directory already exists.")
        else:
            print("ERROR: "+str(e))
    for File in os.listdir(CWD):
        if os.path.isdir(File) == True:
            continue
        if File.endswith(".jpg") or File.endswith(".JPG"):
            print("Valid file: "+File)
            fh = open(File, 'rb')
            try:
                tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
                dateTaken = tags["EXIF DateTimeOriginal"]
                date_taken = str(dateTaken)
                dateStamp = parseDate(date_taken)
                addData(dateStamp, File, foldersAndFiles)
                fh.close()
            except Exception as e:
                print("Error: "+str(e))
                print("Moving problematic file to: "+invalidDir+"/")
                fh.close()
                if os.path.exists(invalidDir+"/"+File):
                    DATE = str(datetime.datetime.now().strftime("%x")).replace('/','-')
                    TIME = str(datetime.datetime.now().strftime("%X")).replace(":",'-')
                    DATETIME_VAR = DATE+"_T"+TIME
                    randFile = os.path.splitext(File)[0]+"_"+DATETIME_VAR+os.path.splitext(File)[1]
                    os.rename(File, randFile)
                    File = randFile
                    shutil.move(File, invalidDir+"/"+randFile)
                else:
                    shutil.move(File, invalidDir+"/")
        elif File.endswith(".py") or File.endswith(".exe"):
            pass
        else:
            print("Invalid file: "+File)
            if os.path.exists(invalidDir+"/"+File):
                DATE = str(datetime.datetime.now().strftime("%x")).replace('/','-')
                TIME = str(datetime.datetime.now().strftime("%X")).replace(":",'-')
                DATETIME_VAR = DATE+"_T"+TIME
                randFile = os.path.splitext(File)[0]+"_"+DATETIME_VAR+os.path.splitext(File)[1]
                os.rename(File, randFile)
                File = randFile
                shutil.move(File, invalidDir+"/")
            else:
                shutil.move(File, invalidDir+"/")

    for key in foldersAndFiles.keys():
        try:
            os.makedirs(key)
        except Exception as e:
            if "Cannot create a file when that file already exists" in str(e):
                print("'"+key+"' directory already exists.")
            else:
                print("Error: "+str(e))
        for img_file in foldersAndFiles[key]:
            if os.path.exists(key+"/"+img_file):
                DATE = str(datetime.datetime.now().strftime("%x")).replace('/','-')
                TIME = str(datetime.datetime.now().strftime("%X")).replace(":",'-')
                DATETIME_VAR = DATE+"_T"+TIME
                randFile = os.path.splitext(img_file)[0]+"_"+DATETIME_VAR+os.path.splitext(img_file)[1]
                os.rename(img_file, randFile)
                img_file = randFile
                shutil.move(img_file, key+"/")
            else:
                shutil.move(img_file, key+"/")

if __name__ == "__main__":
    main()