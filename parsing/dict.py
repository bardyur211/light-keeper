from parsing import tarkov_quests as tq

prapor = {tq.name_quest_prapor[0].text: f'Цель квеста:\n{tq.purpose_proba_pera}\nВыполнение квеста: \n{tq.accomplishment_proba_pera_2}',
          tq.name_quest_prapor[1].text: f'Цель квеста:\n{tq.purpose_proverka_na_vshivost}\nВыполнение квеста: \n{tq.accomplishment_proverka_na_vshivost_3}',
          tq.name_quest_prapor[2].text: f'Цель квеста:\n{tq.purpose_piknik_so_strelboj}\nВыполнение квеста:\n{tq.accomplishment_piknik_so_strelboj}'}


