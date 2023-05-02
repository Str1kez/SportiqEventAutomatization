sql_underway = """
    update event
    set status = 'Идет'
    where starts_at <= now() 
        and now() < ends_at
        and status = 'Запланировано'
        and is_active = true
    returning id;
    """

sql_complete = """
    update event
    set status = 'Завершено'
    where ends_at <= now()
        and status = 'Идет'
        and is_active = true
    returning id, title;
    """

sql_delete = """
    update event
    set is_active = false
    where status = 'Удалено'
        and is_active = true
        and (now() - updated_at) >= interval '%s hour'
    returning id;
    """
