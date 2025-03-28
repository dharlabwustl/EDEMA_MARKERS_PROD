
# from infarct_in_each_aretrial_regions_v2 import *
import sys,os,glob,subprocess,argparse
from infarct_in_each_arterial_regionsNov262024 import *
from binarize_regions_arterial_involvement import *
def clean_dirs():
    command='rm -r /workinginput/*'
    subprocess.call(command,shell=True)
    command='rm -r /maskonly/*'
    subprocess.call(command,shell=True)
    command="rm -r /workingoutput/*"
    subprocess.call(command,shell=True)
    command="rm -r /input/*"
    subprocess.call(command,shell=True)
    command="rm -r /working/*"
    subprocess.call(command,shell=True)
    command="rm -r /ZIPFILEDIR/*"
    subprocess.call(command,shell=True)
    command="rm -r /output/*"
    subprocess.call(command,shell=True)
    command="rm -r /ZIPFILEDIR/*"
    subprocess.call(command,shell=True)
    command="rm -r /NIFTIFILEDIR/*"
    subprocess.call(command,shell=True)
    command="rm -r /DICOMFILEDIR/*"
    subprocess.call(command,shell=True)
    command="rm -r /outputinsidedocker/*"
    subprocess.call(command,shell=True)

def call_arterial_location_distribution(args): #SESSION_ID):
    return_value=0
    try:
        clean_dirs()
        SESSION_ID=args.stuff[1] ##str(row_item['ID'])
        print(SESSION_ID)
        return_value=arterial_region_volumes_n_display(SESSION_ID)
        subprocess.call("echo " + "I call_arterial_location_distribution error  ::{}  >> /workingoutput/error.txt".format(return_value) ,shell=True )

        if return_value==1:
            subprocess.call("echo " + "I call_arterial_location_distribution error  ::{}  >> /workingoutput/error.txt".format(return_value) ,shell=True )
            binarized_region_artery()
        return  return_value

        # error_msg = traceback.format_exc()
        # subprocess.call("echo " + "I traceback error  ::{}  >> /workingoutput/error.txt".format("error_msg") ,shell=True )
    except Exception as e :
        # command = "echo error is " + str(e) + " >>" + "/workingoutput/error.txt"
        # subprocess.call(command,shell=True)
        # print(e)
        # pass
        # except Exception as e :
        # command = "echo error is " + str(e) + " >>" + "/workingoutput/error.txt"
        # subprocess.call(command,shell=True)
        # print(e)
        # pass
        # except Exception as e:
        error_msg = traceback.format_exc()
        subprocess.call("echo " + "I traceback error  ::{}  >> /workingoutput/error.txt".format(error_msg) ,shell=True )
        return 0
def main():
    print("WO ZAI ::{}".format("main"))
    parser = argparse.ArgumentParser()
    parser.add_argument('stuff', nargs='+')
    args = parser.parse_args()
    name_of_the_function=args.stuff[0]
    return_value=0
    if name_of_the_function=="call_arterial_location_distribution":
        return_value=call_arterial_location_distribution(args)

    return  return_value
if __name__ == "__main__":
    main()