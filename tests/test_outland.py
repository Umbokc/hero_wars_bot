class TestOutland:
  mathces = (
    ('main', 'main_open', True),
    ('main_2', 'main_open', True),
    ('main', 'modal_close', True),

    ('highwaymen', 'h_raid', True),
    ('highwaymen_2', 'h_raid', True),
    ('highwaymen_3', 'h_raid', False),

    ('highwaymen', 'modal_close', True),

    ('master', 'go_for_it', True),
    ('master_2', 'go_for_it', True),
    ('master', 'modal_close', True),
    ('master_2', 'modal_close', True),

    ('m_b_open_2', 'modal_close', True),
    ('m_b_open', 'modal_close', True),
    ('m_b_opened', 'modal_close', True),

    ('m_b_open', 'b_open_free', True),

    ('m_f_screen_choose', 'f_to_battle', True),
    ('m_f_screen_done', 'f_open_chest', True),
    ('m_f_screen_fighting', 'f_auto', True),
    ('m_f_screen_fighting_2', 'f_auto', False),

    ('m_open', 'modal_close', True),
    ('m_open', 'm_open_next', True),
    ('m_open_1', 'm_open_next', True),
    ('m_open_2', 'm_open_to_battle', True),

    ('m_open_3', 'main_open', True),
    ('m_open_3', 'main_open', True),

    ('m_open_3', 'm_open_to_battle', False),
    ('m_open_4', 'm_open_to_battle', True),
    ('m_open_5', 'm_open_to_battle', False),

    ('m_open_5', 'm_open_done', True),
    ('m_open_5_2', 'm_open_done', True),
    ('m_open_5_3', 'm_open_done', True),
  )