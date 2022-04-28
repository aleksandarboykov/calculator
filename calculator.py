from tkinter import*
import math

tk = Tk(className='Calculator')

tk.resizable(False, False)

statement = []
prevType = 'none'
result = 0
memory = 0

counter = 0
row = 4
floatNumber = False
pi = 22/7
appended = False


def is_numeric(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def print_test():
    print("(", end=" ")
    for x in range(len(statement)):
        print(statement[x], end=" ")

    print(")", "Memory:", memory, end=" ")
    print()


def primary_calculation(input_a, operation, input_b):
    a = float(input_a)
    b = float(input_b)
    if operation == '+':
        return a + b

    elif operation == '-':
        return a - b

    elif operation == '*':
        return a * b

    elif operation == '/':
        return a / b

    elif operation == '%':
        return a % b

    elif operation == '^':
        return pow(a, b)

    return 0


def unary_calculation(input_a, operation):
    a = float(input_a)
    if operation == 'SQRT':
        return math.sqrt(a)

    elif operation == 'RECP':
        return 1 / a

    elif operation == 'SIGN':
        if a == 0:
            return a
        return -a

    return 0


def clear_statement():
    global statement
    global prevType
    global result
    statement = []
    prevType = "none"
    result = 0


def set_prev_type():
    global prevType
    if len(statement) == 0:
        prevType = 'none'
        return
    if is_numeric(statement[-1]):
        prevType = 'number'
        return
    if statement[-1] in ['+', '-', '*', '/', '%', '^']:
        prevType = 'operation'
        return
    if statement[-1] in ['SQRT', 'RECP', 'SIGN']:
        prevType = 'specialOperation'
        return
    prevType = 'none'


def calculate_pass(operations):
    found = False
    global statement
    i = 0
    stm_copy = []
    while i < len(statement):
        if i < len(statement) - 2 and statement[i + 1] in operations:
            found = True
            res = primary_calculation(statement[i], statement[i + 1], statement[i + 2])
            stm_copy.append(res)
            i += 3
        else:
            stm_copy.append(statement[i])
            i += 1
    statement = stm_copy
    return found


def calculate_priority():
    global statement
    i = 0
    stm_copy = []
    while i < len(statement):
        if i < len(statement)-1 and statement[i+1] in ['SQRT', 'RECP', 'SIGN']:
            res = unary_calculation(statement[i], statement[i+1])
            stm_copy.append(res)
            i += 2
        else:
            stm_copy.append(statement[i])
            i += 1

    found = calculate_pass(['^'])
    while found:
        found = calculate_pass(['^'])

    found = calculate_pass(['*', '/', '%'])
    while found:
        found = calculate_pass(['*', '/', '%'])

    found = calculate_pass(['+', '-'])
    while found:
        found = calculate_pass(['+', '-'])


def calculate():
    global result
    global statement
    global prevType

    try:
        # 0 operand
        if len(statement) == 0:
            return result

        # 1 operand
        if len(statement) == 1:
            result = statement[0]
            return result

        # 2 operand
        if len(statement) == 2:
            # example 5 + =...
            if statement[1] in ['+', '-', '*', '/', '%', '^']:
                if result == 0:
                    result = statement[0]

                result = primary_calculation(result, statement[1], statement[0])
                return result

            if statement[1] in ['SQRT', 'RECP', 'SIGN']:
                result = unary_calculation(statement[0], statement[1])
                clear_statement()
                return result

        calculate_priority()
    except ZeroDivisionError:
        clear_statement()
        print("Cannot divide by zero!")
    if len(statement) > 0:
        result = statement[0]
    else:
        result = 0
    return result


def delete():
    entry.configure(state='normal')
    entry.delete(0, 'end')
    entry.configure(state='readonly')


def delete_and_set(new_value):
    entry.configure(state='normal')
    entry.delete(0, 'end')
    entry.insert(0, new_value)
    entry.configure(state='readonly')


def clear():
    global appended
    global floatNumber
    global counter
    clear_statement()
    appended = False
    floatNumber = False
    set_result(0)
    counter = 0


def clear_entry():
    global appended
    global floatNumber
    global counter
    appended = False
    floatNumber = False
    delete_and_set(0)
    counter = 0


def set_result(number):
    new_result_int = int(number)
    if new_result_int == number:
        delete_and_set(new_result_int)
    else:
        delete_and_set(number)


def on_key_press(a):
    global floatNumber
    global counter
    global statement
    global appended
    if a in ['+', '-', '*', '/', '%', '^']:
        if not appended:
            statement.append(float(entry.get()))
            appended = True
            statement.append(a)
        else:
            statement[-1] = a
        #print_test()
        return
    if '0' <= a <= '9':
        # Don't show more than 1 zero
        if a == '0' and entry.get() == '0':
            return
        if counter == 0 or appended:
            delete()
            appended = False
            floatNumber = False
    if a == '.':
        if appended:
            set_result(0)
            appended = False
            floatNumber = False
        if floatNumber:
            return
        floatNumber = True
    entry.configure(state='normal')
    a = str(a)
    counter += 1
    entry.insert(counter, a)
    entry.configure(state='readonly')


def sign():
    number = entry.get()
    if number == '0':
        return
    if number[0] == '-':
        number = number[1:]
    else:
        number = '-'+number
    delete_and_set(number)


def wurzel_fun():
    global appended
    number = float(entry.get())
    if number == 0:
        return
    if number < 0:
        delete_and_set("Invalid number!")
        appended = True
    if number > 0:
        number = math.sqrt(number)
        set_result(number)


def pow_fun():
    number = float(entry.get())
    number = pow(number, 2)
    set_result(number)


def pow2_fun():
    try:
        number = float(entry.get())
        number = pow(10, number)
        set_result(number)
        float(number)
        return number
    except OverflowError:
        return 0


def pi_fun():
    global pi
    global counter
    statement.append(pi)
    delete_and_set(pi)


def fact_fun():
    global appended
    number = int(entry.get())
    sum = 1
    if number < 0:
        delete_and_set("Invalid number!")
        appended = True
    else:
        while number > 0:
            sum = sum * number
            number = number - 1
        delete_and_set(sum)


def sin_fun():
    symbol = entry.get()
    if is_numeric(symbol):
        symbol = float(symbol)
        symbol = math.sin(symbol)
        if symbol == int(symbol):
            symbol = int(symbol)
        delete_and_set(symbol)


def cos_fun():
    symbol = entry.get()
    if is_numeric(symbol):
        symbol = float(symbol)
        symbol = math.cos(symbol)
        if symbol == int(symbol):
            symbol = int(symbol)
        delete_and_set(symbol)


def tan_fun():
    symbol = entry.get()
    if is_numeric(symbol):
        symbol = float(symbol)
        symbol = math.tan(symbol)
        if symbol == int(symbol):
            symbol = int(symbol)
        delete_and_set(symbol)


def log_fun():
    number = float(entry.get())
    number = math.log(number, 10)
    delete_and_set(number)


def exp_fun():
    number = float(entry.get())
    number = math.exp(number)
    delete_and_set(number)


def gleich_fun():
    #print_test()
    global appended
    if not appended:
        statement.append(float(entry.get()))
        appended = True
    new_result = calculate()
    set_result(new_result)
    statement.append(float(entry.get()))
    appended = True


def ms_fun():
    global memory
    memory = float(entry.get())


def mr_fun():
    global memory
    if memory == int(memory):
        memory = int(memory)
    delete_and_set(memory)


def mc_fun():
    global memory
    memory = 0


def m_plus_fun():
    global memory
    number = float(entry.get())
    if number == int(number):
        number = int(number)
    memory = memory + number


def m_minus_fun():
    global memory
    number = float(entry.get())
    if number == int(number):
        number = int(number)
    memory = memory - number


def rad_fun():
    number = entry.get()
    if '0' <= number <= '9':
        number = float(number)
        number = math.radians(number)
        if number == int(number):
            number = int(number)
    delete_and_set(number)


def deg_fun():
    number = entry.get()
    if '0' <= number <= '9':
        number = float(number)
        number = math.degrees(number)
        if number == int(number):
            number = int(number)
    delete_and_set(number)


def create_button(text, command=0, bg="light grey", state="normal"):
    return Button(tk, text=text, bg=bg, fg="black", relief="flat", width=7, height=1, command=command, state=state)


entry = Entry(tk, state="readonly", fg="black", bg="white", width=43, justify="right", font=('Arial', 10))
entry.grid(row=2, column=0, columnspan=5)

entry.configure(state='normal')
entry.insert(0, '0')
entry.configure(state='readonly')

blank = create_button("", bg="dark grey", state="disabled")
blank.grid(row=3, columnspan=5, sticky="nsew")
blank2 = create_button("", bg="dark grey", state="disabled")
blank2.grid(row=0, columnspan=5, sticky="nsew")
mc = create_button("MC", lambda: mc_fun(), bg="light blue")
mc.grid(row=row, column=0, pady=1)
mr = create_button("MR", lambda: mr_fun(), bg="light blue")
mr.grid(row=row, column=1, pady=1)
mPlus = create_button("M+", lambda: m_plus_fun(), bg="light blue")
mPlus.grid(row=row, column=2, pady=1)
mMinus = create_button("M-", lambda: m_minus_fun(), bg="light blue")
mMinus.grid(row=row, column=3, pady=1)
ms = create_button("MS", lambda: ms_fun(), bg="light blue")
ms.grid(row=row, column=4, pady=1)
row = row+1
pow1 = create_button("x^2", lambda: pow_fun())
pow1.grid(row=row, column=0, pady=1)
pow2 = create_button("x^y", lambda: on_key_press("^"))
pow2.grid(row=row, column=1, pady=1)
sin = create_button("sin", lambda: sin_fun())
sin.grid(row=row, column=2, pady=1)
cos = create_button("cos", lambda: cos_fun())
cos.grid(row=row, column=3, pady=1)
tan = create_button("tan", lambda: tan_fun())
tan.grid(row=row, column=4, pady=1)
row = row+1
wurzel = create_button("√", lambda: wurzel_fun())
wurzel.grid(row=row, column=0, pady=1)
pow3 = create_button("10^x", lambda: pow2_fun())
pow3.grid(row=row, column=1, pady=1)
log = create_button("log", lambda: log_fun())
log.grid(row=row, column=2, pady=1)
exp = create_button("Exp", lambda: exp_fun())
exp.grid(row=row, column=3, pady=1)
mod = create_button("Mod", lambda: on_key_press("%"))
mod.grid(row=row, column=4, pady=1)
row = row+1
blank1 = create_button("", state="disabled")
blank1.grid(row=row, column=0, pady=1)
ce = create_button("CE", lambda: clear_entry())
ce.grid(row=row, column=1, pady=1)
c = create_button("C", lambda: clear())
c.grid(row=row, column=2, pady=1)
blank2 = create_button("", state="disabled")
blank2.grid(row=row, column=3, pady=1)
teilung = create_button("/", lambda: on_key_press("/"))
teilung.grid(row=row, column=4, pady=1)
row = row+1
pi_button = create_button("π", lambda: pi_fun())
pi_button.grid(row=row, column=0, pady=1)
sieben = create_button("7", lambda: on_key_press("7"), bg="white")
sieben.grid(row=row, column=1, pady=1)
acht = create_button("8", lambda: on_key_press("8"), bg="white")
acht.grid(row=row, column=2, pady=1)
neun = create_button("9", lambda: on_key_press("9"), bg="white")
neun.grid(row=row, column=3, pady=1)
multiplikation = create_button("*", lambda: on_key_press("*"))
multiplikation.grid(row=row, column=4, pady=1)
row = row+1
fact = create_button("n!", lambda: fact_fun())
fact.grid(row=row, column=0, pady=1)
fier = create_button("4", lambda: on_key_press("4"), bg="white")
fier.grid(row=row, column=1, pady=1)
funf = create_button("5", lambda: on_key_press("5"), bg="white")
funf.grid(row=row, column=2, pady=1)
sechs = create_button("6", lambda: on_key_press("6"), bg="white")
sechs.grid(row=row, column=3, pady=1)
sub = create_button("-", lambda: on_key_press("-"))
sub.grid(row=row, column=4, pady=1)
row = row+1
zeichen = create_button("+/-", lambda: sign())
zeichen.grid(row=row, column=0, pady=1)
eins = create_button("1", lambda: on_key_press("1"), bg="white")
eins.grid(row=row, column=1, pady=1)
zwei = create_button("2", lambda: on_key_press("2"), bg="white")
zwei.grid(row=row, column=2, pady=1)
drei = create_button("3", lambda: on_key_press("3"), bg="white")
drei.grid(row=row, column=3, pady=1)
add = create_button("+", lambda: on_key_press("+"))
add.grid(row=row, column=4, pady=1)
row = row+1
deg = create_button("DEG", lambda: deg_fun())
deg.grid(row=row, column=0, pady=1)
rad = create_button("RAD", lambda: rad_fun())
rad.grid(row=row, column=1, pady=1)
null = create_button("0", lambda: on_key_press("0"), bg="white")
null.grid(row=row, column=2, pady=1)
punkt = create_button(".", lambda: on_key_press("."))
punkt.grid(row=row, column=3, pady=1)
gleich = create_button("=", lambda: gleich_fun())
gleich.grid(row=row, column=4, pady=1)

tk.configure(bg='grey')

tk.mainloop()

