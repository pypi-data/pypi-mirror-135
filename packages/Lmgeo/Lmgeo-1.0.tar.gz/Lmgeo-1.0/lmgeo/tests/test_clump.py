from lmgeo.toolbox.grouplib import clump
import lmgeo.formats.asciigrid as ag

def main():
    result = None
    try:
        fn = r'D:\\Userdata\\hoek008\\Reuse\\Lmgeo\\input\\grouping_test_case.asc'
        myraster = ag.AsciiGrid(fn, 'i')
        if not myraster.open('r'):
            raise Exception("Unable top open file " + fn)
        
        result = clump(myraster, -9)
        if not result is None:
            print(result.data)
    
    except Exception as e:
        print(e)
    finally:
        if not myraster is None:
            myraster.close()
            
if __name__ == "__main__":
    main()
