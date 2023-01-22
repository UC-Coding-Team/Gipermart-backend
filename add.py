# Ro'yhatdan o'tishni yozish uchun list va dictionary
# kabi datatipni ishlatamiz

# Ro'yhatga kirish uchun list yaratamiz
royhat = []

while True:
    # Foydalanuvchi ma'lumotlarini so'ralaymiz
    ism = input("Ismingizni kiriting: ")
    familiya = input("Familiyangizni kiriting: ")
    yosh = input("Yoshingizni kiriting: ")

    # Ma'lumotlarni ro'yhatga qo'shaymiz
    royhat.append({
        'Ism': ism,
        'Familiya': familiya,
        'Yosh': yosh
    })
    # Ro'yhatni chiqarish uchun so'rov
    chiqish = input("Ro'yhatdan chiqmoqchi bo'lsangiz 'chiqish' yozing: ")
    if chiqish == 'chiqish':
        break

# Ro'yhatni chiqarish
for i in royhat:
    print(i)