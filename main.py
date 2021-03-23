import tkinter as tk

import mysql.connector


class GUI:
    def __init__(self):
        self.messages = []
        # Creating the window.
        self.root = tk.Tk()
        self.root.title('PyPiep')

        # Creating frames.
        self.left_f = tk.Frame()
        self.right_f = tk.Frame()

        self.left_f.grid(row=0, column=0, sticky='nsew', padx=(20, 10))
        self.right_f.grid(row=0, column=1, sticky='nsew', padx=(10, 20))

        self.message_label = tk.Label(self.left_f, text='Bericht')
        self.message_text = tk.Text(self.left_f, width=40, height=5,
                                    wrap=tk.WORD)
        self.bericht_button = tk.Button(self.left_f, text='Piep it!',
                                        command=self.piep_it, height=1)

        self.filter_label = tk.Label(self.right_f, text='Filter op #')
        self.filter_text = tk.Text(self.right_f, width=40, height=5,
                                   wrap=tk.WORD)
        self.filter_button = tk.Button(self.right_f, text='Ververs!',
                                       command=self.get_pieps, height=1)

        self.piep_list = tk.Listbox(self.right_f, height=5, width=75)
        self.piep_message = tk.Text(self.right_f, height=10, width=57)
        # self.likes_label.pack(side='top', anchor='nw')

        self.message_label.pack(side='top', anchor='nw')
        self.message_text.pack(side='left', anchor='nw', padx=(5, 10))
        self.bericht_button.pack(side='left', anchor='n')

        self.piep_message.pack(side='bottom', anchor='w', pady=10)
        self.piep_list.pack(side='bottom', anchor='w')
        self.piep_list.bind("<<ListboxSelect>>", self.show_message)

        self.filter_label.pack(side='top', anchor='nw')
        self.filter_text.pack(side='left', anchor='nw', pady=(0, 10))
        self.filter_button.pack(side='left', anchor='ne')

        tk.mainloop()

    def piep_it(self):
        query = 'insert into piep(bericht) values(%s)'
        message = str(self.message_text.get("1.0", "end-1c"))
        cursor.execute(query, [message])

    def get_pieps(self):
        self.piep_message.delete('1.0', 'end')
        search = self.filter_text.get("1.0", "end-1c").replace(' ',
                                                               '').split(
            ',')
        if search:
            formatted = []
            search_iter = iter(search)
            formatted.append(f"p.bericht REGEXP "
                             f"\'{next(search_iter)}([^A-Za-z0-9]|$)\'")
            for tag in search_iter:
                formatted.append(
                    f" and p.bericht REGEXP \'{tag}([^A-Za-z0-9]|$)\'")
            formatted = ''.join(formatted)

            cursor.execute('select p.piep_id, p.bericht, s.voornaam, '
                           's.tussenvoegsels,'
                           's.achternaam, DATE_FORMAT(p.tijd, '
                           '\'%H:%i\') '
                           'from piep p '
                           'natural join student s '
                           f'where {formatted}'
                           ' order by p.piep_id desc')
        else:
            cursor.execute('select p.piep_id, p.bericht, s.voornaam, '
                           's.tussenvoegsels,'
                           's.achternaam, DATE_FORMAT(p.tijd, '
                           '\'%H:%i\') '
                           'from piep p '
                           'natural join student s '
                           'order by p.piep_id desc')

        results = cursor.fetchall()
        self.messages = []
        self.piep_list.delete(0, 'end')
        for piep_id, bericht, vn, tv, an, time in results:
            if not tv:
                tv = ' '
            else:
                tv = f' {tv} '
            # reformatted.append(f'{vn}{tv}{an} om\n')
            # reformatted.append(f'\t{bericht}\n')
            # reformatted.append(f'Gepiept om {time}')
            self.messages.append((piep_id, bericht))
            self.piep_list.insert('end', f'{vn}{tv}{an} om {time}')

    def show_message(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            message = self.messages[index][1]
            self.piep_message.delete('1.0', 'end')
            self.piep_message.insert('end', message)


if __name__ == '__main__':
    params = {'host': '145.74.104.145', 'user': 'okcum', 'db': 'okcum',
              'password': 'Aa657680!',
              'auth_plugin': 'mysql_native_password'}
    with mysql.connector.connect(**params) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SET autocommit = ON')
            GUI()  # menu()
