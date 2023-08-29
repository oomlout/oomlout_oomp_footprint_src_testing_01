import oomlout_footprint_src as oom_f_s
import oom_kicad 

def main():
    #set a start time using time
    import time
    starttime = time.time()
    oom_f_s.make_footprint_yaml()
    oom_f_s.clone_and_copy_footprints()
    oom_f_s.make_footprints_readme()
    #print the time it took to complete
    print('That took {} seconds'.format(time.time() - starttime))
    oom_kicad.push_to_git()





if __name__ == '__main__':
    main()