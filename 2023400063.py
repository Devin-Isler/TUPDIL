output = ""
def main():
    # DO NOT CHANGE
    global output
    handle = open('input.tup')
    code = handle.read()
    handle.close()
    code = code.rstrip("\n")
    sentences = code.split("\n")
    var_val = {} # var_name: which line a value is assigned to it
    var_typ = {} # {var_name: type}
    variables = {} # {var_name: [val,type]}

    start = "programı başlat."
    end = "programı bitir."
    turkish_letters = [
    'A', 'B', 'C', 'Ç', 'D', 'E', 'F', 'G', 'Ğ', 'H', 'I', 'İ', 'J', 'K', 'L', 'M', 'N', 'O', 'Ö', 'P', 'R', 'S', 'Ş', 'T', 'U', 'Ü', 'V', 'Y', 'Z',
    'a', 'b', 'c', 'ç', 'd', 'e', 'f', 'g', 'ğ', 'h', 'ı', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'ö', 'p', 'r', 's', 'ş', 't', 'u', 'ü', 'v', 'y', 'z'
]   
    other = [" ", ",", ".", ":", ";"]
    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    operators = ["artı", "eksi", "bölü", "çarp"]
    keywords = operators + ["metin", "reel-sayı", "tam-sayı", "bir", "olsun", "zıpla", "satıra", "yazdır", "değeri", "programı", "bitir", "başlat"]
    types = ["reel-sayı", "tam-sayı", "metin"]

    # Split spaces but skips if the space is between two "!" 
    def my_split(str_=""):
        str_ = str_.strip(" ")
        counter = 0
        for char in str_:
            if "!" == char:
                counter += 1

        if counter % 2 != 0:
            return False
        
        if counter == 0:
            return str_.split()
        
        lst = []
        lst_str = list(str_)
        i = 0
        j = 0
        while i != len(lst_str):
            if lst_str[i] == "!":
                while True:
                    i += 1
                    if lst_str[i] == "!":
                        i += 1
                        break

            elif lst_str[i] == " ":
                lst.append("".join(lst_str[j:i]))
                i += 1
                j = i
            else:
                i += 1
        else:
            lst.append("".join(lst_str[j:]))
        return lst
    # Lower entire turkish sentence except between two "!"
    def my_lower(s=""):
        word = ""
        check = True
        for letter in s:
            if letter == "!":
                check = not check
                word += letter
                continue
            if check:
                if letter not in ["İ","I"]:
                    word += letter.lower()
                elif letter == "I":
                    word += "ı"
                elif letter == "İ":
                    word += "i"
            else:
                word += letter 
        return word
    # Helps while converting metin to reel
    def my_replace(s=""):
        return s.replace(".","?").replace(",",".").replace("?",",")
    # Check if has any consecutive spaces expect between "!"
    def has_consecutive_spaces(s):
        if_inside = False
        space_found = False

        i = 0
        while i < len(s)-1:
            if s[i] == '!':
                if_inside = not if_inside
            elif not if_inside and s[i] == ' ':
                if s[i + 1] == ' ':
                    space_found = True
                    break
            i += 1
        return space_found 
    # Check if vairable name is valid
    def check_var_name(var):
        if var in keywords:
            return False
        if len(var) > 20:
            return False
        for char in var:
            if char not in turkish_letters + operators:
                return False
        return True
    # Check if given type is valid
    def is_type_valid(typ):
        return typ in types
    # Returns to type of the value
    def what_type(val=""):
        if val[0] == val[-1] == "!":
            return "metin"
        
        if "," in val:
            try:
                float(val.replace(".","").replace(",","."))
                return "reel-sayı"
            except ValueError:
                pass

        try:
            int(val.replace(".",""))
            return "tam-sayı" 
        except ValueError:
            pass
        return "değişken"
    # Check if it is valid tam-sayı
    def check_tam_sayı(n=""):
        if n[0] == "-":
            n = n[1:]
        if n[0] == ".":
            return False
        for i in n:
            if i not in digits + ["."]:
                return False
        if n.count(".") > 1:            
            return False
        if "." in n:
            if len(n) < 4:
                return False
        if len(n) > 3:
            if n[-4] != ".":
                return False
        if int(n.replace(".","")) > 10000:
            return False
        return True
    # Check if it is valid reel-sayı
    def check_reel_sayı(n=""):
            try:
                int_, dec = n.split(",")
            except ValueError:
                return False
            if len(dec) > 3:
                return False
            if not check_tam_sayı(int_):
                return False
            if float(int_.replace(".","") + "." + dec) > 10000 or float(int_.replace(".","") + "." + dec) < -10000:
                return False
            return True
    # Check if it is valid metin
    def check_metin(n=""):
        if n.count("!") != 2:
            return False
        n = n.strip("!")
        if len(n) > 50:
            return False
        for char in n:
            if char not in turkish_letters + other + digits:
                return False
        return True
    
    check_types = {"tam-sayı": check_tam_sayı, "reel-sayı": check_reel_sayı, "metin": check_metin}
    # Check if given value can be converted to tam-sayı
    def convertable_to_tam(n=""):
        n = n.strip("!")
        if "," in n:
            if not check_reel_sayı(n):
                return False
            try:
                n_ = float(n.replace(".","").replace(",","."))
            except ValueError:
                return False
            return int(n_) == n_

        if check_tam_sayı(n):
            return True

        else:
            return False
    # Check if given value can be converted to tam-sayı
    def convertable_to_reel(n=""):
        n = n.strip("!")
        if check_reel_sayı(n):
            return True
        else:
            return False
    # Check if the operators are valid
    def check_operators(expr=[]):
        for i in range(len(expr)):
            if i % 2 == 1:
                if expr[i] not in operators:
                    return False
        return True
    # Check if the constant is valid
    def check_constant(s=""):
        typ_ = what_type(s)
        return check_types[typ_](s)
    # Check if all the constants in an expression is valid
    def check_constants(expr=[]):
        if not check_operators(expr):
            return False

        for i in range(len(expr)):
            if i % 2 == 0:
                constant = expr[i]
                if not check_constant(constant):
                    return False
        return True
    # Check if all variable name in an expression is valid
    def check_variables(expr=[]):
        var_list = []
        if not check_operators(expr):
            return False
        for i in range(len(expr)):
            if i % 2 == 0:
                var = expr[i]
                if check_var_name(var) == False:
                    return False
            var_list.append(var)
        return var_list
    # Changes the constants in the expression with their types
    def convert_type_list(expr=[]):
        return_list = []
        for i in range(len(expr)):
            if i % 2 == 0:
                constant = expr[i]
                return_list.append(what_type(constant))
            else:
                return_list.append(expr[i])
        return return_list
    # Define what types can be processed with what type
    def operator_on_types(x="",y="",oper=""):
        if oper == "artı" or oper == "eksi":
            if x == y:
                return x
            elif (x == "metin" and y == "tam-sayı") or (x == "tam-sayı" and y == "metin"):
                return "tam-sayı"
            elif (x == "metin" and y == "reel-sayı") or (x == "reel-sayı" and y == "metin"):
                return "reel-sayı"
            else:
                return False
        elif oper == "bölü" or oper == "çarp":
            if x == y == "tam-sayı":                
                return "reel-sayı"
            elif x == y == "reel-sayı":
                return x
            elif oper == "çarp" and ((x == "metin" and y == "tam-sayı") or (x == "tam-sayı" and y == "metin")):
                return "metin"
            elif oper == "bölü" and ((x == "metin" and y == "tam-sayı") or (x == "tam-sayı" and y == "metin")):
                return "reel-sayı"
            elif (x == "metin" and y == "reel-sayı" or x == "reel-sayı" and y == "metin"):
                return "reel-sayı"
            else:
                return False
    # Check if the expression is valid by looking types
    def type_expressions(l=[]):
        type_expr = convert_type_list(l)
        length = len(type_expr)
        if length == 1:
            return True
        elif length % 2 == 0:
            return False
        else:
            for _ in range((len(type_expr)-1)//2):
                left = type_expr[0]
                oper = type_expr[1]
                right = type_expr[2]

                typ_ = operator_on_types(right,left,oper)
                if typ_ == False:
                    return False
                type_expr[0:3] = [typ_]
            return True
    # Convert to tam-sayı
    def convert_to_tam(s=""):
        s = s.strip("!").replace(".","").replace(",",".")
        return int(float((s)))
    # Convert reel-sayı
    def convert_to_reel(s=""):
        s = s.strip("!").replace(".","").replace(",",".")
        return float(s)
    # Checks if an expression valid for the zıpla
    def is_it_valid_zıpla(n=""):
        typ_ = what_type(n)
        n = n.strip("!")
        if n[0] == "-":
            return False
        elif typ_ == "tam-sayı":
            return int(n.replace(".",""))
        elif typ_ == "reel-sayı":
            n = float((n.replace(".","").replace(",",".")))
            if int(n) == float(n):
                return int(n)
        elif typ_ == "metin":
            if convertable_to_tam(n):
                n = n.replace(".","").replace(",",".")
                return int(float((n)))
            else:
                return False
        elif typ_ == "değişken":
            return True
        return False
    # Adding functon
    def artı(x,y):
        return x + y
    # Substracting functon
    def eksi(x,y):
        return x - y
    # Multiplying functon
    def çarp(x,y):
        return x * y
    # Dividing functon
    def bölü(x,y):
        return x / y
    # Substracting to metins
    def metin_eksi(v1="",v2=""):
        l1 = len(v1)
        l2 = len(v2)
        
        if l1 < l2:
            return
        to_be_deleted = list()
        for i in range(l1 - l2 + 1):
            x = True
            temp = list()
            for j in range(l2):
                if v2[j] == v1[i]:
                    temp.append(i)
                    i += 1
                    continue
                else:
                    x = False
                    break
            if x:
                for item in temp:
                        if item not in to_be_deleted:
                            to_be_deleted.append(item)
        list_ = list(v1)
        for k in range(l1-1 ,-1 ,-1):
            if k in to_be_deleted:
                list_.pop(k)
        return "".join(list_)
    # Checking if the given value is 0
    def check_0(n=""):
        typ_ = what_type(n)
        n = n.strip("!")
        if typ_ == "tam-sayı":
            num = int(n.replace(".",""))
        elif typ_ == "reel-sayı":
            num = float((n.replace(".","").replace(",",".")))
        elif typ_ == "metin":
            if convertable_to_tam(n):
                n = n.replace(".","").replace(",",".")
                num = float(n)
            else:
                return False
        if num == 0:
            return True
        return False
    # Defining the calculations for the given expression
    def artı_eksi(x="", y="", oper=""):
        typ_x = what_type(x)
        typ_y = what_type(y)

        opers = {"artı": artı, "eksi": eksi}
        if typ_x == typ_y == "tam-sayı":
            x_ = x.replace(".", "")
            y_ = y.replace(".", "")
            return f"{opers[oper](int(x_),int(y_)):,}".replace(",",".")
        
        elif typ_x == typ_y == "metin":
            x_ = x.strip("!")
            y_ = y.strip("!")
            if oper == "artı":
                return "!" + x_ + y_ + "!"
            else:
                return "!" + metin_eksi(x_,y_) + "!"

        elif typ_x == typ_y == "reel-sayı":
            x_ = float(x.replace(".","").replace(",",".")) * 1000
            y_ = float(y.replace(".","").replace(",",".")) * 1000
            return my_replace(f"{(opers[oper](x_,y_)) / 1000 :,}")

        elif (typ_x == "tam-sayı" and typ_y == "metin") or (typ_y == "tam-sayı" and typ_x == "metin"):
            if not convertable_to_tam(x) or not convertable_to_tam(y):
                return False
            x_ = convert_to_tam(x)
            y_ = convert_to_tam(y)
            return f"{opers[oper](int(x_),int(y_)):,}".replace(",",".")
        
        elif (typ_x == "reel-sayı" and typ_y == "metin") or (typ_y == "reel-sayı" and typ_x == "metin"):
            if not convertable_to_reel(x) or not convertable_to_reel(y):
                return False
            x_ = convert_to_reel(x) * 1000
            y_ = convert_to_reel(y) * 1000
            return my_replace(f"{(opers[oper](x_,y_)) / 1000 :,}")
    # Defining the calculations for the given expression
    def çarp_bölü(x="", y="", oper=""):
        typ_x = what_type(x)
        typ_y = what_type(y)
        opers = {"çarp": çarp, "bölü": bölü}

        if oper == "bölü" and check_0(y):
            return False
        elif typ_x == typ_y == "tam-sayı":
            x_ = x.replace(".", "")
            y_ = y.replace(".", "")
            return my_replace(f"{float(opers[oper](int(x_),int(y_))):,}")
        
        elif typ_x == typ_y == "reel-sayı" and oper == "çarp":
            x_ = float(x.replace(".","").replace(",",".")) * 1000
            y_ = float(y.replace(".","").replace(",",".")) * 1000
            return my_replace(f"{(x_* y_) / 1000000:,}")
        
        elif typ_x == typ_y == "reel-sayı" and oper == "bölü":
            x_ = float(x.replace(".","").replace(",",".")) * 1000
            y_ = float(y.replace(".","").replace(",",".")) * 1000
            return my_replace(f"{(x_ / y_):,}")
        
        elif (typ_x == "tam-sayı" and typ_y == "metin") and oper == "çarp":
            x_ = x.replace(".", "")
            y_ = y.strip("!")
            return "!" + int(x_) * y_ + "!"
        
        elif (typ_y == "tam-sayı" and typ_x == "metin") and oper == "çarp":
            y_ = y.replace(".", "")
            x_ = x.strip("!")
            return "!" + int(y_) * x_ + "!"
        
        elif (typ_x == "tam-sayı" and typ_y == "metin") or (typ_y == "tam-sayı" and typ_x == "metin") and oper == "bölü":
            if not convertable_to_tam(x) or not convertable_to_tam(y):
                return False
            x_ = convert_to_tam(x) * 1000
            y_ = convert_to_tam(y) * 1000
            return my_replace(f"{float(opers[oper](int(x_),int(y_))):,}")

        elif (typ_x == "reel-sayı" and typ_y == "metin") or (typ_y == "reel-sayı" and typ_x == "metin"):
            if not convertable_to_reel(x) or not convertable_to_reel(y):
                return False
            if oper == "çarp":
                x_ = convert_to_reel(x) * 1000
                y_ = convert_to_reel(y) * 1000
                return my_replace(f"{(x_* y_) / 1000000:,}")
            else:
                x_ = convert_to_reel(x) * 1000
                y_ = convert_to_reel(y) * 1000
                return my_replace(f"{x_ / y_:,}")

    operations = {"artı":artı_eksi, "eksi":artı_eksi, "çarp":çarp_bölü, "bölü":çarp_bölü}
    # Does the calculations dor given expression
    def operation_with_constant(expr=[]):
        for _ in range((len(expr)-1)//2):
            left = expr[0]
            oper = expr[1]
            right = expr[2]
            result = operations[oper](left,right,oper)
            
            if not result:
                return False

            if not check_constant(result):
                return False
            
            expr[0:3] = [result]
        return expr[0]
    # Check if the variable is defined before
    def is_variable_exist(var=""):
        if var not in variables or variables[var][0] == False:
            return False
        return True
    # Convert all variables to their values 
    def convert_var_to_const(expr=[]):
        lst = []
        for i in range(len(expr)):
            if i % 2 == 1:
                lst.append(expr[i])
            else:
                if is_variable_exist(expr[i]):
                    lst.append(variables[expr[i]][0])
                else:
                    return False
        return lst
    # Check if the variables value is given before
    def var_val_(var="", n=0):
        if var not in var_val:
            var_val[var] = n

    compile_error = False
    #Compile Errors
    for i in range(len(sentences)):
        sentence = my_lower(sentences[i])
        words = my_split(sentence)
        line = i+1
        # Checks if the first sentence is start
        if i == 0:
            if start != sentence:
                compile_error = True
                break
            continue
        # Checks if the second last sentence is end
        elif i == len(sentences) - 1:
            if sentence != end:
                compile_error = True
                break
            continue
        # Checks if the line is empty
        if not words:
            compile_error = True
            break
        # Checks if is the sentence to short to be valid
        elif len(words) < 2:
            compile_error = True
            break
        # Chech the end of the sentences
        elif sentence[-1] != "." or sentence[0] == " ":
            compile_error = True
            break
        # Check if there is unwanted consecutive spaces
        elif has_consecutive_spaces(sentence):
            compile_error = True
            break
        # Check if there is a compile in "the defining variable" sentences
        elif words[1] == "bir" and words[-1] == "olsun.":
            var = words[0]
            if len(words) != 4 or not check_var_name(var):
                compile_error = True
                break

            typ = words[2]
            if not is_type_valid(typ):
                compile_error = True
                break
            var_typ[var] = typ
        # Check if there is a compile in "the giving value to a variable" sentences
        elif words[1] == "değeri" and words[-1] == "olsun.":
            var1 = words[0]
            if not check_var_name(var1) or len(words) < 4:
                compile_error = True
            expr1 = words[2:-1]
            if what_type(expr1[0]) != "değişken":
                if not check_constants(expr1) or not type_expressions(expr1):
                    compile_error = True
                    break
            else:
                lst1 = check_variables(expr1)
                if not lst1:
                    compile_error = True
                    break                
                for v in lst1:
                    var_val_(v,line)
            var_val_(var1, line)
        # Check if there is a compile in the "zıpla" sentences
        elif words[-2] == "satıra" and words[-1] == "zıpla.":
            expr2 = " ".join(words[:-2])
            if expr2[-1] != "." or len(words) < 3:
                compile_error = True
                break 
            expr2 = expr2[:-1].split(" ")
            if what_type(expr2[0]) != "değişken":
                if not check_constants(expr2) or not type_expressions(expr2):
                    compile_error = True
                    break
            else:
                lst2 = check_variables(expr2)
                if not lst2:
                    compile_error = True
                    break
                for v in lst2:
                    var_val_(v, line)

            if len(expr2) == 1:
                const = is_it_valid_zıpla(expr2[0])
                if not const:
                    compile_error = True
                    break
                if const > len(sentences):
                    compile_error = True
                    break
        # Check if there is a compile in the "yadır" sentences
        elif words[-1] == "yazdır.":
            expr3 = words[:-1]
            if what_type(expr3[0]) != "değişken":
                if not check_constants(expr3) or not type_expressions(expr3):
                    compile_error = True
                    break
            else:
                lst1 = check_variables(expr3)
                if not lst1:
                    compile_error = True
                    break
                for v in lst1:
                    var_val_(v,line)
        # If the sentence doesn't fit any sentence, then compile error
        else:
            compile_error = True
            break
    # For last, check if an undefined variable is used by comparing (defined variables)-(value given variable) dictinoaries
    if not compile_error:
        for var in var_val:
            if var not in var_typ:
                line = var_val[var]
                compile_error = True
                break
    if compile_error:
        output = f"Compile error at line {line}.\n"
    else:
        runtime_error = False
        #Running the Program
        j = 0
        while j < len(sentences):
            sentence = my_lower(sentences[j])
            words = my_split(sentence)
            line = j+1

            if j == 0 or j == len(sentences)-1:
                j += 1
                continue 
            # Adds the variable to the dictinary
            if words[1] == "bir" and words[-1] == "olsun.":
                var = words[0]
                variables[var] = [False, words[-2]]
            #  Adding the value to the dictinary, checks if it is defined and also if the value is the specified type
            elif words[1] == "değeri" and words[-1] == "olsun.":
                var1 = words[0]
                if var1 not in variables:
                    runtime_error = True
                    break

                expr1 = words[2:-1]
                if what_type(expr1[0]) == "değişken":
                    expr1 = convert_var_to_const(expr1)
                    if not expr1:
                        runtime_error = True
                        break
                result = operation_with_constant(expr1)
                if not result:
                    runtime_error = True
                    break
                check = what_type(result)
                if check != variables[var1][1]:
                    runtime_error = True
                    break
                
                variables[var1][0] = result 
            # Checks if expressions is valid or not, if valid changes the j to jump.
            elif words[-2] == "satıra" and words[-1] == "zıpla.":
                expr2 = " ".join(words[:-2])
                expr2 = expr2[:-1].split(" ")
                if what_type(expr2[0]) == "değişken":
                    expr2 = convert_var_to_const(expr2)   
                    if not expr2:
                        runtime_error = False
                        break                 
                result = operation_with_constant(expr2)
                if not result:
                    runtime_error = True
                    break
                x = is_it_valid_zıpla(result)
                if not x:
                    runtime_error = True
                    break
                if x > len(sentences):
                    runtime_error = True
                    break
                j = x - 1
                continue
            # If valid, print the statement to terminal
            elif words[-1] == "yazdır.":
                expr3 = words[:-1]
                if not expr3:
                    runtime_error = True
                    break
                if what_type(expr3[0]) == "değişken":
                    expr3 = convert_var_to_const(expr3)
                    if not expr3:
                        runtime_error = True
                        break
                result = operation_with_constant(expr3)
                if not result:
                    runtime_error = True
                    break
                output += result.strip("!") + "\n"
            j += 1
        if runtime_error:
            output += f"Runtime error at line {line}.\n"

    # DO NOT CHANGE
    handle = open('output.txt','w')
    handle.write(output)
    handle.close()

main()