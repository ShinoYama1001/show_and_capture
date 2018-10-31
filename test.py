with open("setting.txt") as setting:
        user_name = setting.readline().strip()
        dir_name = setting.readline().strip()
        dir_info = [i.split() for i in setting.readlines()]

        print(user_name)
        print(dir_name)
        print(dir_info)