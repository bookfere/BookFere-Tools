#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, sys, glob, shutil, datetime, re, codecs

#fix ''ascii' codec can't decode byte 0xe8 in position ...'
if sys.version_info.major < 3:
    reload(sys)
    sys.setdefaultencoding('utf-8')

# Define
cleanshot = False
cleanlog  = True

# Process
def onProcess(kindlePath) :
    documentsPath = kindlePath + '/documents'
    checkDocumentsPathVer = os.path.exists(documentsPath)

    logFile = documentsPath + '/sdrCleaner_log.txt'
    if( os.path.exists( logFile ) ) :
        os.remove( logFile )

    if checkDocumentsPathVer == False :
        sys.exit(0)

    list_dirs = os.walk(documentsPath)
    root_dirs = os.listdir(kindlePath)

    sdr_list_s = ''
    sdr_list_f = ''
    dir_list_s = ''
    dir_list_f = ''
    scs_list = ''

    sdr_s_count = 0
    sdr_f_count = 0
    dir_s_count = 0
    dir_f_count = 0
    shot_count = 0

    clean = False

    # Clean Screen Shot
    if cleanshot == True :
        for files in root_dirs:
            if ( files[:10] == 'screenshot' and files[-4:] == '.png' ) or ( files[:18] == 'wininfo_screenshot' and files[-4:] == '.txt'):
                os.chdir(kindlePath)
                os.remove(files)
                #仅统计图片
                if files[:10] == 'screenshot' and files[-4:] == '.png':
                    scs_list += u'\u25cf ' + files +'\n'
                    shot_count += 1
                    clean = True

    # Clean SDR Folder
    for root, dirs, files in list_dirs:
        for numb in dirs:
            if numb:
                os.chdir(root)

                sdr = glob.glob(r'*.sdr')
                _dir = glob.glob(r'*.dir')
                azw = glob.glob(r'*.azw')
                azw3 = glob.glob(r'*.azw3')
                pdf = glob.glob(r'*.pdf')
                txt = glob.glob(r'*.txt')
                prc = glob.glob(r'*.prc')
                mobi = glob.glob(r'*.mobi')
                pobi = glob.glob(r'*.pobi')
                epub = glob.glob(r'*.epub')
                azw4 = glob.glob(r'*.azw4')
                kfx = glob.glob(r'*.kfx')

                format_sdr = False
                format_dir = False

                for unsdr in sdr:
                    if unsdr[-4:] == '.sdr':
                        format_sdr = True
                        break

                for undir in _dir:
                    if undir[-4:] == '.dir':
                        format_dir = True
                        break

                if format_sdr == True:
                    for unsdr in sdr:
                        sdr_self = os.path.dirname(os.path.abspath('__file__'))
                        if unsdr[-4:] == sdr_self[-4:]:
                            continue
                        found = False
                        for n1 in azw:
                            if unsdr[:-4] == n1[:-4]:
                                found = True
                                break
                        for n2 in azw3:
                            if unsdr[:-4] == n2[:-5]:
                                found = True
                                break
                        for n3 in pdf:
                            if unsdr[:-4] == n3[:-4]:
                                found = True
                                break
                        for n4 in txt:
                            if unsdr[:-4] == n4[:-4]:
                                found = True
                                break
                        for n5 in prc:
                            if unsdr[:-4] == n5[:-4]:
                                found = True
                                break
                        for n6 in mobi:
                            if unsdr[:-4] == n6[:-5]:
                                found = True
                                break

                        for n7 in pobi:
                            if unsdr[:-4] == n7[:-5]:
                                found = True
                                break
                        for n8 in epub:
                            if unsdr[:-4] == n8[:-5]:
                                found = True
                                break
                        for n9 in kfx:
                            if unsdr[:-4] == n9[:-4]:
                                found = True
                                break
                        for n10 in azw4:
                            if unsdr[:-4] == n10[:-5]:
                                found = True
                                break
                        if found == False:
                            try:
                                shutil.rmtree(unsdr)
                                if unsdr == 'sdrCleaner_log.sdr' :
                                    continue
                            except OSError:
                                sdr_f_count += 1
                                sdr_list_f += u'\u25cf ' + unsdr +'\n'
                            else:
                                sdr_s_count += 1
                                sdr_list_s += u'\u25cf ' + unsdr +'\n'
                            clean = True

                if format_dir == True:
                    for undir in _dir:
                        dir_self = os.path.dirname(os.path.abspath('__file__'))
                        if undir[-4:] == dir_self[-4:]:
                            continue
                        found = False
                        for n1 in azw:
                            if undir[:-8] == n1[:-4]:
                                found = True
                                break
                        for n2 in azw3:
                            if undir[:-9] == n2[:-5]:
                                found = True
                                break
                        for n3 in pdf:
                            if undir[:-8] == n3[:-4]:
                                found = True
                                break
                        for n4 in txt:
                            if undir[:-8] == n4[:-4]:
                                found = True
                                break
                        for n5 in prc:
                            if undir[:-8] == n5[:-4]:
                                found = True
                                break
                        for n6 in mobi:
                            if undir[:-9] == n6[:-5]:
                                found = True
                                break
                        for n7 in pobi:
                            if undir[:-9] == n7[:-5]:
                                found = True
                                break
                        for n8 in epub:
                            if undir[:-9] == n8[:-5]:
                                found = True
                                break
                        for n9 in kfx:
                            if undir[:-8] == n9[:-4]:
                                found = True
                                break
                        for n10 in azw4:
                            if undir[:-9] == n10[:-5]:
                                found = True
                                break
                        if found == False:
                            try:
                                shutil.rmtree(undir)
                                if undir == 'sdrCleaner_log.dir' :
                                    continue
                            except OSError:
                                dir_f_count += 1
                                dir_list_f += u'\u25cf ' + undir +'\n'
                            else:
                                dir_s_count += 1
                                dir_list_s += u'\u25cf ' + undir +'\n'
                            clean = True
                break

    # Generate Clean Log
    if clean == True and cleanlog == True:

        sdr_s_count_str = str(sdr_s_count)
        sdr_f_count_str = str(sdr_f_count)
        dir_s_count_str = str(dir_s_count)
        dir_f_count_str = str(dir_f_count)
        shot_count_str = str(shot_count)

        now = datetime.datetime.now()
        nowStyle = now.strftime('%Y-%m-%d %H:%M:%S')
        new_log = open(logFile,'w')
        new_log.write('清理时间 ' + nowStyle + '\n=================================\n')
        if sdr_list_s :
            new_log.write('共删除成功 ' + sdr_s_count_str +' 个无用 SDR 文件夹：\n---------------------------------\n')
            new_log.write(sdr_list_s)
            new_log.write('=================================\n')
        if sdr_list_f :
            new_log.write('有 ' + sdr_f_count_str + ' 个 SDR 文件夹没有删除成功：\n---------------------------------\n')
            new_log.write(sdr_list_f)
            new_log.write('=================================\n')
        if dir_list_s :
            new_log.write('共删除成功 ' + dir_s_count_str +' 个无用 DIR 文件夹：\n---------------------------------\n')
            new_log.write(dir_list_s)
            new_log.write('=================================\n')
        if dir_list_f :
            new_log.write('有 ' + dir_f_count_str + ' 个 DIR 文件夹没有删除成功：\n---------------------------------\n')
            new_log.write(dir_list_f)
            new_log.write('=================================\n')
        if sdr_list_f or dir_list_f :
            new_log.write('* 删除失败是因为该文件名中含有特殊字符无法被删除，目前还没找到好的办法解决，请暂时手动删除。\n')
            new_log.write('---------------------------------\n')
        if scs_list :
            new_log.write('共删除成功 ' + shot_count_str +' 个截图：\n---------------------------------\n')
            new_log.write(scs_list)
            new_log.write('=================================\n')
        new_log.write('书伴 - 为静心阅读而生\nhttps://bookfere.com')
        new_log.close()

# Execute
if __name__ == '__main__':
    onProcess('/chroot/mnt/us/')