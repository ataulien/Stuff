def stringifySequences(id_list):
        """ Turns the given ID-List into a pretty string usable by dplace, for example.
            A list of [1,2,3,4,8] will be turned into "1-4,8" """
            
        id_list = sorted(id_list)
        
        s = ""
        last = -1
        for i in id_list:
            if len(s) == 0:
                s = str(i)
            else:
                # Check if we are on a running sequence
                if i == last + 1:
                    if s[-1] != '-':
                        s += '-'
                    # If we already have the '-', do nothing while inside the sequence
                else:
                    # Place sequence end
                    if s[-1] == '-':
                        s += str(last)
            
                    # Put the new starting point
                    s += "," + str(i)
            
            last = i
            
        
        if len(s) and s[-1] == '-':
            s += str(last)
            
        return s
        
def formatByteSize(bytes):
    if bytes < 1024:
        return str(bytes) + " bytes";
    elif bytes < 1024 * 1024:
        return str(round(bytes / 1024.0)) + " KB";
    elif bytes < 1024 * 1024 * 1024:
        return str(round(bytes / (1024.0 * 1024.0))) + " MB";
    elif bytes < 1024 * 1024 * 1024 * 1024:
        return str(round(bytes / (1024.0 * 1024.0 * 1024))) + " GB"; 
    elif bytes < 1024 * 1024 * 1024 * 1024 * 1024:
        return str(round(bytes / (1024.0 * 1024.0 * 1024 * 1024))) + " TB";     