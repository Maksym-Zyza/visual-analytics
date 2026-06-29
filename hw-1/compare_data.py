import pandas as pd

def compare_excel_files(old_path, new_path):
    print("Завантаження таблиць для порівняння...\n")
    df_old = pd.read_excel(old_path, sheet_name=0)
    df_new = pd.read_excel(new_path, sheet_name=0)

    print("=== 1. ЗАГАЛЬНІ ЗМІНИ РОЗМІРУ ===")
    print(f"Оригінал: {df_old.shape[0]} рядків, {df_old.shape[1]} стовпців")
    print(f"Очищено:  {df_new.shape[0]} рядків, {df_new.shape[1]} стовпців\n")

    print("=== 2. ЗМІНИ У СТОВПЦЯХ ===")
    dropped_cols = set(df_old.columns) - set(df_new.columns)
    if dropped_cols:
        print(f"Видалені стовпці: {', '.join(dropped_cols)}\n")
    else:
        print("Стовпці не видалялися.\n")

    print("=== 3. ПОШУК ЗМІНЕНИХ ЗНАЧЕНЬ ===")
    # Метод df.compare() вимагає, щоб обидві таблиці мали абсолютно однакові 
    # розміри та індекси. Оскільки ми видаляли рядки з помилками, 
    # прямий df_old.compare(df_new) видасть помилку (ValueError).
    #
    # Тому ми порівнюємо лише ті рядки та стовпці, які залишилися в обох таблицях:
    
    # Залишаємо тільки спільні стовпці
    common_cols = list(set(df_old.columns) & set(df_new.columns))
    df_old_common = df_old[common_cols]
    df_new_common = df_new[common_cols]

    # Вирівнюємо таблиці по індексах, щоб порівнювати тільки ті рядки, що не були видалені
    # Ми беремо індекси з очищеного датафрейму, оскільки він менший
    common_indices = df_new_common.index.intersection(df_old_common.index)
    
    df_old_aligned = df_old_common.loc[common_indices].sort_index(axis=1)
    df_new_aligned = df_new_common.loc[common_indices].sort_index(axis=1)

    # Тепер можемо безпечно використати compare()
    diff = df_old_aligned.compare(df_new_aligned)
    
    if diff.empty:
        print("Не знайдено жодних змінених значень у спільних рядках.")
    else:
        print(f"Знайдено змінені значення (виправлені помилки) у {len(diff)} рядках.")
        print("Ось кілька прикладів змін (self = було, other = стало):")
        print(diff.head(10))

if __name__ == "__main__":
    compare_excel_files("Go IT Data_Cleaned.xlsx", "Zyza_Maksym_Go IT Data.xlsx")
