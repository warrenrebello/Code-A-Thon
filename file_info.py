import requests
import json
import os
import time
import schedule


class FileData:
    def __init__(self):
        pass

    # This function will allow us to get the info of each file within the director
    def getData(self):

        os.chdir('C:\Python')
        all_files = filter(os.path.isfile, os.listdir())
        data = {}

        for each in all_files:
            date_m = time.ctime(os.path.getmtime(each))
            date_c = time.ctime(os.path.getctime(each))
            file_size = os.path.getsize(each)
            file_info = each.split('.')
            item = {each:[date_c, date_m, file_info[0], file_info[1], file_size]}
            data.update(item)

        return data

    # This function will store the data into a JSON file, and then read from that file
    def convertJson(self, file_name):

        data = self.getData()

        with open(file_name + ".json", "w") as f:
            json.dump(data, f)

        with open(file_name + ".json", "r") as myFile:
            file_data = myFile.read()

        return file_data

    # This function will display the data from the JSON file
    def displayData(self):

        file_data = self.convertJson("NewJson")

        obj = json.loads(file_data)
        keys = obj.keys()

        print("{:<40}{:<30}{:<30}{:30}{:<10}{:<8}" .format('File', 'Date Modified', 'Date Created', 'Name', 'Ext', 'Size'))
        print()

        for each in keys:
            print("{:<40}{:<30}{:<30}{:30}{:<10}{:<8}" .format(each, obj[each][0], obj[each][1], obj[each][2], obj[each][3], obj[each][4]))

        self.existing = file_data
        self.compareData()

    '''def scanFiles():
        print("I'm working...")

        schedule.every(1).seconds.do(job)

        while True:
            schedule.run_pending()
            time.sleep(1)
    '''
    def compareData(self):
        changed = self.convertJson("Changed")
        
        existing_obj = json.loads(self.existing)
        existing_keys = existing_obj.keys()

        changed_obj = json.loads(changed)
        changed_keys = changed_obj.keys()

        result = True

        length = len(changed_keys)-1
        n = 0
        newList = list(existing_keys)
        for each in changed_keys:
            if each == newList[n]:
                each_length = len(each)
                m = 0
                for items in changed_obj[each]:
                    if items == existing_obj[each][m]:
                        pass
                    else:
                        result = False
                        print("Data Changed")
                        break
                m += 1
            else:
                result = False
                print("Data Changed")
                break
        n += 1