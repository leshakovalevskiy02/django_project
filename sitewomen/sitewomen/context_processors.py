def get_women_context(request):
    menu = [{'title': "О сайте", 'url_name': 'about'},
            {'title': "Добавить статью", 'url_name': 'add_page'},
            {'title': "Обратная связь", 'url_name': 'contact'},
            {'title': "Войти", 'url_name': 'users:login', 'title2': "Регистрация", 'url_name2': "home"}
            ]

    if request.user.is_authenticated:
        menu[-1] = {'title': f"{request.user.username}", 'title2': "Выйти", 'url_name2': "users:logout"}

    return {"mainmenu": menu}