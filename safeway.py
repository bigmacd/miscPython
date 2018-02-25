import requests
import time
from json import JSONDecodeError
import argparse

# McLean Rate Center is Washington Zone 17, VA
# Great Falls Rate Center is Washington Zone 19, VA
# LATA is 236
# ILEC is 9213
# http://localcallingguide.com/lca_exch.php?exch=205040 (17)
# http://localcallingguide.com/lca_exch.php?exch=205050 (19)

Zone17_NPA_NXX = {
    571: [205, 221, 226, 230, 235, 238, 241, 244, 245, 249, 251, 253,
          263, 265, 268, 269, 282, 286, 294, 296, 297, 314, 326, 327, 
          331, 332, 335, 337, 338, 341, 355, 356, 369, 378, 382, 385, 
          389, 395, 405, 419, 421, 422, 423, 424, 425, 468, 472, 488, 
          489, 499, 501, 502, 505, 533, 550, 565, 570, 581, 594, 620, 
          623, 633, 635, 641, 651, 666, 722, 730, 749, 765, 766, 830, 
          835, 839, 999], 
    703: [200, 204, 205, 206, 207, 208, 226, 231, 237, 238, 241, 245, 
          256, 269, 270, 275, 285, 286, 287, 288, 289, 300, 315, 316, 
          320, 321, 333, 336, 342, 343, 354, 356, 371, 377, 388, 394, 
          400, 442, 448, 451, 452, 462, 485, 506, 531, 532, 533, 534, 
          536, 538, 556, 559, 560, 564, 568, 569, 573, 582, 584, 585, 
          587, 593, 597, 598, 599, 610, 635, 637, 639, 641, 642, 644, 
          645, 655, 658, 663, 675, 676, 677, 698, 712, 714, 720, 725, 
          731, 734, 738, 744, 747, 748, 749, 750, 752, 760, 761, 762, 
          770, 776, 786, 790, 798, 813, 821, 827, 839, 846, 847, 848, 
          849, 852, 854, 855, 861, 862, 863, 864, 866, 867, 868, 869, 
          873, 876, 883, 891, 893, 899, 902, 903, 905, 912, 913, 914, 
          916, 917, 918, 923, 940, 941, 942, 962, 970, 981, 983, 992]
}

Zone19_NPA_NXX = {
    571: [201, 204, 224, 234, 278, 279, 280, 295, 307, 308, 318, 328,
          340, 350, 354, 363, 373, 386, 418, 432, 435, 455, 459, 474,
          490, 495, 512, 529, 585, 723, 732, 748, 789, 992],
    703: [218, 219, 222, 223, 225, 227, 242, 246, 251, 255, 259, 261,
          262, 264, 265, 267, 268, 272, 273, 277, 279, 280, 281, 293,
          295, 318, 319, 322, 323, 324, 326, 332, 344, 345, 349, 352,
          359, 364, 374, 375, 383, 384, 385, 386, 389, 397, 404, 406,
          424, 425, 426, 438, 449, 450, 453, 456, 459, 460, 471, 478,
          482, 484, 487, 502, 503, 537, 539, 561, 563, 589, 591, 592,
          613, 620, 621, 631, 633, 636, 638, 648, 652, 653, 654, 667,
          679, 691, 708, 709, 713, 715, 716, 733, 735, 736, 742, 755,
          757, 758, 759, 764, 766, 788, 802, 803, 808, 810, 818, 833,
          834, 865, 874, 877, 890, 896, 904, 925, 934, 937, 938, 944,
          947, 948, 968, 978, 991, 993, 995]
}

phoneNumber = "{NPA}{NXX}{:0>4}"
url = "https://www.safeway.com/rss/service/validator/ccphone/{0}"

interRequestDelay = 0.2

def doZone(npa, inNxx, outFile):
    zoneData = None
    if npa == 17:
        zoneData = Zone17_NPA_NXX[inNxx]
    else:
        zoneData = Zone19_NPA_NXX[inNxx]
    recordCount = 0
    with open(outFile , "w") as outfile:
        for nxx in zoneData:
            for i in range(0, 10000):
                number = phoneNumber.format(i, NPA=inNxx, NXX=nxx)
                thisUrl = url.format(number)
                try:
                    r = requests.get(thisUrl)
                    if r.status_code == 200:
                        try:
                            data = r.json()
                            if data['isValid'] == True:
                                outfile.write("{0}\n".format(number))
                                recordCount = recordCount + 1
                                if recordCount % 1000 == 0:
                                    outfile.flush()
                        except JSONDecodeError:
                            print ("faild to decode json: {0}".format(r.text))
                except:
                    print("caught exception, carrying on...")
                time.sleep(interRequestDelay)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--zone", type = int)
    parser.add_argument("--npa", type = int)
    parser.add_argument("--outfile")
    args = parser.parse_args()
    assert((args.zone ==  17 or args.zone == 19) == True)
    assert((args.npa == 571 or args.npa == 703) == True)
    doZone(args.zone, args.npa, args.outfile)