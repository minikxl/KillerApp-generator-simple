import random, smtplib, ssl
from email.message import EmailMessage
from getpass import getpass

Base = {}

def menu():
    print('='*30)
    print('\tKiller-app')
    print('='*30)
    print('''
    1. Dodawanie użytkowników do bazy
    2. Wyświetlenie bazy danych
    3. Wysyłanie maili

Kliknij enter, aby zakończyć program.
    ''')
    ask = input('Co chcesz zrobić >>> ')
    if ask == '1':
        addToBase()
    elif ask == '2':
        print("\nBaza danych:")
        for a, b in Base.items():
            print("\t{} -> email: {}".format(a,b))
        input()
    elif ask == '3':
        send()
    else:
        exit(0)
    menu()

def addToBase():
    print('='*30)
    print('\tDodawanie do bazy')
    print('='*30)
    print('Proszę podać dane w formacie:\n\tImię Nazwisko, e-mail\n')
    ask = True
    while ask != '':
        ask = input('(Imie Nazwisko, e-mail) >> ')
        try:
            name, mail = ask.split(', ')
            if name in Base:
                if input('Ta osoba już istnieje w bazie. Czy chcesz ją nadpisać?(T/N): ').upper() == 'Y':
                    print("Nadpisano")
                    Base[name] = mail
                else:
                    print("Pozostawiono bez zmian")

            else:        
                Base[name] = mail
        except ValueError:
            print('Błąd. Spróbuj ponownie używając odpowiedniego formatu')
    else:
        print('Baza została zaktualizowana...')
    
def generate():
    Peoples = list(Base.keys())
    rand_Peoples = random.sample(Peoples, len(Peoples))
    couples = []

    for i in range(len(rand_Peoples)):
        if i != len(rand_Peoples)-1:
            couples.append((rand_Peoples[i], rand_Peoples[i+1]))
        else:
            couples.append((rand_Peoples[i], rand_Peoples[0]))

    return couples

def send():
    print('='*35)
    print('\tWysyłanie wiadomości')
    print('='*35)
    startDate, startHour = (input("Podaj godzinę rozpoczęcia gry: "), input("Podaj datę rozpoczęcia gry: "))
    print('\n\tlogowanie do serwera pocztowego...\n')
    login = input("Podaj swój adres e-mail: ")
    serv = input("Podaj adres serwera smtp: ")
    password = getpass("Podaj hasło: ")

    sender = "KILLER-APP <{}>".format(login)
    port = 465  # For SSL
    # Create a secure SSL context
    context = ssl.create_default_context()

    for c in generate():
        receiver = Base[c[0]]
        msg = EmailMessage()
        msg['Subject'] = "KILLER - losowanko"
        msg['From'] = sender
        msg['To'] = receiver
        msg.set_content("""Hello {}! 
Rozpoczynamy grę w killera!!!

\t Twój cel to: {}
\t Grę zaczynamy od godziny {} ({}).\n

Zasady gry:
    Waszym zadaniem jest wyeliminować swój cel. Możecie to zrobić, poprzez podanie mu dowolnej rzeczy (w domyśle przedmiotu) z ręki do ręki.
    Zabójca bierze cel martwego i planuje kolejne morderstwo. Wygrywa osoba, która dotrwa do końca i będzie miała najwięcej zabójstw.

--------------------------------------------------\n
Wiadomość została wygenerowana automatycznie. Prosimy na nią nie odpowiadać. 
KillerGenerator by Dominik Kras""".format(c[0], c[1], startHour, startDate))

        try:
            with smtplib.SMTP_SSL(serv, port, context=context) as server:
                server.login(login, password)
                server.send_message(msg)

            print('Wysyłam do: {}'.format(receiver))
        except smtplib.SMTPServerDisconnected:
            print('Nie można połączyć z serwerem. Zły login/hasło/adres serwera?')
        except smtplib.SMTPException as e:
            print('Wystąpił błąd SMTP: ' + str(e))
    
if __name__ == "__main__":
    
    menu()

    


