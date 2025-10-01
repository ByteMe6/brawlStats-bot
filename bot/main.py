# pip install brawlstats

import brawlstats

client = brawlstats.Client("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjNkNmQ1Y2Y4LWM5N2EtNDA1Yi04N2JkLTU0NzYwNjA2YTgxNSIsImlhdCI6MTc1ODU2NzQ1NCwic3ViIjoiZGV2ZWxvcGVyL2UzOTU5YzY3LWJlN2YtYWFiMS1mNDRlLTg1ODRhOTg0YWU5MiIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTI4LjEyNy4xMjcuNDEiXSwidHlwZSI6ImNsaWVudCJ9XX0.wyypdUvE4nIogqYtmNr7px0H0agW2xxknPSvG6Lqn-63dm2o1G-iCYtolp_gx6pzaedZamIPSsR2_remxjx0zg") # type: ignore

profile = client.get_profile("#90PGJRQCQ")

print('------ ОСНОВНАЯ ИНФОРМАЦИЯ ------')
print(f"{profile.name} | {profile.tag}\n") 
print(f"Цвет ника: {profile.name_color}")
print(f"Кубки: {profile.trophies} (Рекорд: {profile.highest_trophies})")
print(f"Уровень: {profile.exp_level} (Опыт: {profile.exp_points})")

print('\n------ РЕЖИМЫ ------')
print(f"Победы 3 на 3: {profile.x3vs3_victories}")
print(f"Одиночные победы: {profile.solo_victories}")
print(f"Парные победы: {profile.duo_victories}")

print('\n------ БОЙЦЫ ------')
# Получаем список всех бойцов игрока
brawlers = profile.brawlers

# Сортируем бойцов по количеству кубков (от большего к меньшему)
brawlers_sorted = sorted(brawlers, key=lambda x: x.trophies, reverse=True)

print(f"Всего бойцов: {len(brawlers)}")

# РАСЧЕТ ПРОГРЕССА ПРОКАЧКИ
COINS_PER_MAX_BRAWLER = 17765  # Базовая: уровни + 1 гаджет(1000) + 1 пассивка(2000) + 2 снаряжения(2000) + гиперзаряд(5000)
COINS_PER_MAX_BRAWLER_FULL = 24765  # Полная: + дополнительно 1 гаджет(1000) + 1 пассивка(2000) + 3 снаряжения(3000)

# Общие затраты на весь аккаунт (для 103 бойцов)
TOTAL_COINS_FULL_ACCOUNT = 103 * COINS_PER_MAX_BRAWLER_FULL
TOTAL_POWER_POINTS_FULL_ACCOUNT = 336600  # 103 бойца × 3270 очков силы

# Подсчитываем статистику
maxed_brawlers = 0
total_coins_spent = 0
total_coins_spent_full = 0
total_power_points_spent = 0

# Считаем общее количество гаджетов, звёздных сил и снаряжений
total_gadgets = 0
total_star_powers = 0
total_gears = 0

for brawler in brawlers:
    # Расчет затрат на уровни (1-11 уровень = 11765 монет)
    if brawler.power == 1:
        coins_for_levels = 0
    else:
        coins_for_levels = min(11765, (brawler.power - 1) * (11765 / 10))
    
    # Получаем количество снаряжений (gears)
    gears_list = getattr(brawler, 'gears', [])
    gears_count = len(gears_list) if hasattr(gears_list, '__len__') else 0
    
    # БАЗОВАЯ прокачка: уровни + 1 гаджет + 1 пассивка + 2 снаряжения + гиперзаряд
    gadgets_count_base = min(len(brawler.gadgets), 1)  # Только 1 гаджет для базовой
    star_powers_count_base = min(len(brawler.star_powers), 1)  # Только 1 пассивка для базовой
    gears_count_base = min(gears_count, 2)  # Максимум 2 снаряжения
    
    # Стоимость базовой прокачки
    coins_spent_base = coins_for_levels
    coins_spent_base += gadgets_count_base * 1000  # 1 гаджет
    coins_spent_base += star_powers_count_base * 2000  # 1 пассивка  
    coins_spent_base += gears_count_base * 1000  # 2 снаряжения (по 1000 каждое)
    
    # Если боец 11 уровня, добавляем стоимость гиперзаряда (5000)
    if brawler.power == 11:
        coins_spent_base += 5000
    
    total_coins_spent += min(coins_spent_base, COINS_PER_MAX_BRAWLER)
    
    # ПОЛНАЯ прокачка: всё то же самое + дополнительно 1 гаджет + 1 пассивка + 3 снаряжения
    gadgets_count_full = min(len(brawler.gadgets), 2)  # Все 2 гаджета
    star_powers_count_full = min(len(brawler.star_powers), 2)  # Все 2 пассивки
    gears_count_full = min(gears_count, 5)  # Все 5 снаряжений
    
    coins_spent_full = coins_for_levels
    coins_spent_full += gadgets_count_full * 1000  # 2 гаджета
    coins_spent_full += star_powers_count_full * 2000  # 2 пассивки
    coins_spent_full += gears_count_full * 1000  # 5 снаряжений
    
    # Если боец 11 уровня, добавляем стоимость гиперзаряда (5000)
    if brawler.power == 11:
        coins_spent_full += 5000
    
    total_coins_spent_full += min(coins_spent_full, COINS_PER_MAX_BRAWLER_FULL)
    
    total_gadgets += len(brawler.gadgets)
    total_star_powers += len(brawler.star_powers)
    total_gears += gears_count
    
    # Расчет очков силы
    power_points_spent = min(3270, (brawler.power - 1) * 327)
    total_power_points_spent += power_points_spent
    
    if brawler.power == 11:
        maxed_brawlers += 1

# Расчет прогресса для базовой прокачки
total_coins_needed = len(brawlers) * COINS_PER_MAX_BRAWLER
coins_remaining = max(0, total_coins_needed - total_coins_spent)
progress_percentage = min(100, (total_coins_spent / total_coins_needed) * 100) if total_coins_needed > 0 else 0

# Расчет прогресса для полной прокачки
total_coins_needed_full = len(brawlers) * COINS_PER_MAX_BRAWLER_FULL
coins_remaining_full = max(0, total_coins_needed_full - total_coins_spent_full)
progress_percentage_full = min(100, (total_coins_spent_full / total_coins_needed_full) * 100) if total_coins_needed_full > 0 else 0

# Расчет прогресса очков силы
power_points_remaining = max(0, TOTAL_POWER_POINTS_FULL_ACCOUNT - total_power_points_spent)
power_points_progress = min(100, (total_power_points_spent / TOTAL_POWER_POINTS_FULL_ACCOUNT) * 100) if TOTAL_POWER_POINTS_FULL_ACCOUNT > 0 else 0

print(f"\n--- ПРОГРЕСС ПРОКАЧКИ ---")
print(f"Максимально прокачанных бойцов: {maxed_brawlers}/{len(brawlers)}")
print(f"Всего гаджетов: {total_gadgets}/{len(brawlers) * 2}")
print(f"Всего звёздных сил: {total_star_powers}/{len(brawlers) * 2}")
print(f"Всего снаряжений: {total_gears}/{len(brawlers) * 5}")

print(f"\n● БАЗОВАЯ ПРОКАЧКА (до 11 уровня + 1 гаджет + 2 снаряжения + 1 пассивка + гиперзаряд):")
print(f"Потрачено монет: ~{int(total_coins_spent):,} из {int(total_coins_needed):,}")
print(f"Осталось монет: ~{int(coins_remaining):,}")
print(f"Прогресс: {progress_percentage:.1f}%")

# Визуализация прогресса базовой прокачки
bar_length = 20
filled_length = int(bar_length * progress_percentage / 100)
bar = '█' * filled_length + '░' * (bar_length - filled_length)
print(f"[{bar}] {progress_percentage:.1f}%")

print(f"\n● ПОЛНАЯ ПРОКАЧКА (11 ур. + гипер + 2 гаджета + 2 зв.силы + 5 снаряжений):")
print(f"Потрачено монет: ~{int(total_coins_spent_full):,} из {int(total_coins_needed_full):,}")
print(f"Осталось монет: ~{int(coins_remaining_full):,}")
print(f"Прогресс: {progress_percentage_full:.1f}%")

# Визуализация прогресса полной прокачки
filled_length_full = int(bar_length * progress_percentage_full / 100)
bar_full = '█' * filled_length_full + '░' * (bar_length - filled_length_full)
print(f"[{bar_full}] {progress_percentage_full:.1f}%")

print(f"\n● ОЧКИ СИЛЫ:")
print(f"Потрачено очков силы: ~{int(total_power_points_spent):,} из {TOTAL_POWER_POINTS_FULL_ACCOUNT:,}")
print(f"Осталось очков силы: ~{int(power_points_remaining):,}")
print(f"Прогресс: {power_points_progress:.1f}%")

# Визуализация прогресса очков силы
filled_length_pp = int(bar_length * power_points_progress / 100)
bar_pp = '█' * filled_length_pp + '░' * (bar_length - filled_length_pp)
print(f"[{bar_pp}] {power_points_progress:.1f}%")

print(f"\n💡 ДЛЯ СПРАВКИ:")
print(f"Полная прокачка всего аккаунта ({len(brawlers)}/103 бойцов):")
print(f"- Требуется монет: {TOTAL_COINS_FULL_ACCOUNT:,}")
print(f"- Требуется очков силы: {TOTAL_POWER_POINTS_FULL_ACCOUNT:,}")
print(f"- Стоимость одного бойца: {COINS_PER_MAX_BRAWLER_FULL:,} монет")

# Статистика по уровням бойцов
level_distribution = {}
for brawler in brawlers:
    level = brawler.power
    level_distribution[level] = level_distribution.get(level, 0) + 1

print(f"\n--- РАСПРЕДЕЛЕНИЕ БОЙЦОВ ПО УРОВНЯМ ---")
for level in sorted(level_distribution.keys(), reverse=True):
    count = level_distribution[level]
    percentage = (count / len(brawlers)) * 100
    coins_for_level = min(11765, (level - 1) * (11765 / 10))
    print(f"Уровень {level}: {count} бойцов ({percentage:.1f}%) | ~{int(coins_for_level):,} монет на уровни")

print("\nТоп-5 бойцов по кубкам: (Этот сезон)")
for i, brawler in enumerate(brawlers_sorted[:5], 1):
    print(f"{i}. {brawler.name}: {brawler.trophies} кубков | Уровень силы {brawler.power}")

if brawlers:
    best_brawler = brawlers_sorted[0]
    print(f"\n--- Статистика - {best_brawler.name} ---")
    print(f"Кубки (макс.): {best_brawler.trophies} ({best_brawler.highest_trophies})")
    print(f"Уровень силы: {best_brawler.power}")
    print(f"Ранг: {best_brawler.rank}")
    print(f"Звёздные силы: {len(best_brawler.star_powers)}/2")
    print(f"Гаджеты: {len(best_brawler.gadgets)}/2")
    
    # Получаем количество снаряжений для лучшего бойца
    best_brawler_gears = getattr(best_brawler, 'gears', [])
    best_brawler_gears_count = len(best_brawler_gears) if hasattr(best_brawler_gears, '__len__') else 0
    print(f"Снаряжения: {best_brawler_gears_count}/5")
    
    # Прогресс прокачки этого бойца
    if best_brawler.power == 1:
        coins_spent = 0
    else:
        coins_spent = min(11765, (best_brawler.power - 1) * (11765 / 10))
    
    coins_spent += min(len(best_brawler.gadgets), 1) * 1000
    coins_spent += min(len(best_brawler.star_powers), 1) * 2000
    coins_spent += min(best_brawler_gears_count, 2) * 1000
    
    if best_brawler.power == 11:
        coins_spent += 5000
    
    coins_spent_full = coins_spent
    coins_spent_full += max(0, min(len(best_brawler.gadgets) - 1, 1)) * 1000
    coins_spent_full += max(0, min(len(best_brawler.star_powers) - 1, 1)) * 2000
    coins_spent_full += max(0, min(best_brawler_gears_count - 2, 3)) * 1000
    
    brawler_progress = min(100, (coins_spent / COINS_PER_MAX_BRAWLER) * 100)
    brawler_progress_full = min(100, (coins_spent_full / COINS_PER_MAX_BRAWLER_FULL) * 100)
    
    print(f"Прогресс базовой прокачки: {brawler_progress:.1f}%")
    print(f"Прогресс полной прокачки: {brawler_progress_full:.1f}%")

print("\n------ КЛУБ ------")
if profile.club:
    club = client.get_club(profile.club.tag)
    
    club_type = club.type
    if club_type == "open":
        club_type = "Открытый"
    elif club_type == "inviteOnly":
        club_type = "По приглашению"
    elif club_type == "closed":
        club_type = "Закрытый"
    
    print(f"{club.name} | {club.tag}\n")
    print(f"Тип: {club_type}")
    print(f"Кубки: {club.trophies} (Треб. для входа: {club.required_trophies})")
    print(f"Участники: {len(club.members)}/30")
    print(f"Описание: {club.description}\n")

    # Исправленная сортировка участников
    def sort_members(member):
        role_priority = {"president": 4, "vicePresident": 3, "senior": 2, "member": 1}
        return (role_priority.get(member.role, 0), -member.trophies)
    
    members_sorted = sorted(club.members, key=sort_members, reverse=True)

    print("--- Участники (Топ-5 по кубкам) ---")
    role_translation = {"president": "Президент", "vicePresident": "Вице-президент", "senior": "Ветеран", "member": "Участник"}
    
    for member in members_sorted[:5]:
        role = role_translation.get(member.role, member.role)
        print(f"{member.name} - {role} - {member.trophies} кубков")

    print("\n--- Все Участники ---")
    for member in members_sorted:
        role = role_translation.get(member.role, member.role)
        print(f"{member.name} - {role} - {member.trophies} кубков")
