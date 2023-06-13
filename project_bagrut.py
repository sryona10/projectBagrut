import socket
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import time
import os
import pandas as pd
from threading import Thread

task_counter = 0
PATH = os.path.join(os.path.dirname(__file__), 'table.csv')
PORT = 5081
IP = "127.0.0.1"


def main():
    def change_name():
        window.title(entry.get() + "'s schedule")

    def button_click():
        button.invoke()

    def change_frame(current_frame, frame_name):
        current_frame.pack_forget()
        frame_name.pack()

    def get_info():
        global task_counter
        task_counter += 1
        if task_counter <= 20:
            try:
                print(task_counter)
                start_time = start_time_box.get()
                end_time = end_time_box.get()

                if int(start_time[:2]) < int(end_time[:2]):
                    task_time = f'{start_time} - {end_time}'
                    tasks.insert("", tk.END, values=(task_time, subject_box.get(), notes_box.get()))
                    update_csv(task_time, subject_box.get(), notes_box.get())
                    time_saver.set(time_saver.get() + "\n" + start_time + "-" + end_time)
                    subject_saver.set(subject_saver.get() + "\n" + subject_box.get())
                    notes_saver.set(notes_saver.get() + "\n" + notes_box.get())
                else:
                    erroring("start time is bigger than end time")
                    # raise Exception("start time is bigger than end time")

            except ValueError:
                print('invalid time')
                erroring("invalid time")

        else:
            erroring("too much events")

    def create_csv():
        if not os.path.isfile(PATH):
            with open(PATH, 'w') as f:
                f.write('TIME,SUBJECT,NOTES')
        else:
            with open(PATH, 'w') as f:
                f.write('TIME,SUBJECT,NOTES')

        pass

    def update_csv(t, task, notes):
        # df = pd.read_csv(PATH)
        # temp_df = pd.DataFrame([[t, task, notes]], columns=['TIME', 'SUBJECT', 'NOTES'])
        # df.concat([df, temp_df], ignore_index=True)
        # df.to_csv(PATH)

        with open(PATH, "a") as file:
            file.write(f"\n{t},{task},{notes}")

    def export_file():
        filepath = filedialog.askdirectory()
        with open(f"{filepath}\Timefix.csv", 'w') as f:
            df = pd.read_csv(PATH)
            df.to_csv(f"{filepath}\Timefix.csv")

    def erroring(text):
        tk.messagebox.showerror(title='Python Error', message=text)

    def clear_boxes():
        start_time_box.delete(0, len(start_time_box.get()))
        start_time_box.insert(0, end_time_box.get())
        end_time_box.delete(0, len(end_time_box.get()))
        subject_box.delete(0, len(subject_box.get()))
        notes_box.delete(0, len(notes_box.get()))

    def submit_data():
        get_info()
        clear_boxes()

    def submit_name():
        is_name_ok = check()
        if is_name_ok:
            change_name()
            change_frame(entry_frame, second_frame)

    def check():
        if entry.get() == "":
            erroring("you did not set a name")
            return False
        return True
        # raise Exception("UNCORECT NAME")

    def receive():
        while True:
            msg = client_socket.recv(1024).decode()
            messages_box.insert(tk.END, f"expert: {msg}")
            print("message received")

    # connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    client_socket.send("client".encode())
    print("connected to the server")

    create_csv()
    window = tk.Tk()
    window.configure(bg="light blue")

    # קביעת כותרת לחלון
    window.title("timefix")

    # קביעת גודל לחלון
    window.geometry("1000x700")

    # string vars

    time_saver = tk.StringVar(window)
    subject_saver = tk.StringVar(window)
    notes_saver = tk.StringVar(window)
    eror1 = tk.StringVar(window)
    eror2 = tk.StringVar(window)
    eror3 = tk.StringVar(window)
    msg_var = tk.StringVar()
    # frames create
    entry_frame = tk.Frame(window, width=1000, height=700, bg="light blue")
    entry_frame.pack()
    second_frame = tk.Frame(window, width=1000, height=700, bg="light blue")
    chat_frame = tk.Frame(window, width=1000, height=700, bg="light blue")

    # eror text

    eror_lable_1 = tk.Label(entry_frame, textvariable=eror1, font=("Arial", 13, "bold"), foreground="red",
                            anchor="center", justify="center", bg="light blue")
    eror_lable_2 = tk.Label(second_frame, textvariable=eror2, font=("Arial", 13, "bold"), foreground="red",
                            anchor="center", justify="center", bg="light blue")
    eror_lable_3 = tk.Label(chat_frame, textvariable=eror3, font=("Arial", 13, "bold"), foreground="red",
                            anchor="center", justify="center", bg="light blue")
    eror_lable_1.place(relx=0.5, rely=0.5, anchor="center")
    eror_lable_2.place(relx=0.5, rely=0.5, anchor="center")
    eror_lable_3.place(relx=0.5, rely=0.5, anchor="center")

    # חלון כניסה

    # הוספת כותרת לחלון
    big_label = tk.Label(entry_frame, text="Hello dear user, wellcom to timefix!", font=("Arial", 15, "bold"),
                         foreground="blue", anchor="center", justify="center", bg="light blue")
    big_label.place(relx=0.5, rely=0.05, anchor="center")

    small_lable = tk.Label(entry_frame, text="whats your name?", font=("Arial", 13, "bold"), foreground="green",
                           anchor="center", justify="center", bg="light blue")
    small_lable.place(relx=0.5, rely=0.1, anchor="center")

    # יצירת תיבת טקסט
    entry = tk.Entry(entry_frame, width=30)
    entry.place(relx=0.5, rely=0.15, anchor="center", height=20)

    # יצירת כפתור
    button = tk.Button(entry_frame, text="submit",
                       command=lambda: submit_name())
    entry.bind("<Return>", lambda event: button_click())
    button.place(relx=0.5, rely=0.2, anchor="center")
    # second screen

    # button sumbit
    button2 = tk.Button(second_frame, text="submit", command=lambda: submit_data())
    button2.place(relx=0.55, rely=0.95, anchor="center")

    # chat button
    button_chat = tk.Button(second_frame, text="go to chat with expert",
                            command=lambda: [change_frame(second_frame, chat_frame)])
    button_chat.place(relx=0.9, rely=0.95, anchor="center")

    # erase all button
    erase_button = tk.Button(second_frame, text="erase all")
    erase_button.place(relx=0.45, rely=0.95, anchor="center")

    # time
    time_lable = tk.Label(second_frame, text="please set time for the current task", font=("Arial", 13, "bold"),
                          foreground="green", anchor="center", justify="center", bg="light blue")
    time_lable.place(relx=0.5, rely=0.05, anchor="center")

    b_label = tk.Label(second_frame, text="starting time", font=("Arial", 11, "bold"), foreground="purple",
                       anchor="center", justify="center", bg="light blue")
    b_label.place(relx=0.4, rely=0.1, anchor="center")

    b_label = tk.Label(second_frame, text="ending time", font=("Arial", 11, "bold"), foreground="purple",
                       anchor="center", justify="center", bg="light blue")
    b_label.place(relx=0.6, rely=0.1, anchor="center")

    start_time_box = tk.Entry(second_frame, width=20)
    start_time_box.place(relx=0.4, rely=0.13, anchor="center")

    end_time_box = tk.Entry(second_frame, width=20)
    end_time_box.place(relx=0.6, rely=0.13, anchor="center")

    # subject
    subject_label = tk.Label(second_frame, text="please set subject for the current task", font=("Arial", 13, "bold"),
                             foreground="green", anchor="center", justify="center", bg="light blue")
    subject_label.place(relx=0.5, rely=0.18, anchor="center")

    subject_box = tk.Entry(second_frame, width=35)
    subject_box.place(relx=0.5, rely=0.22, anchor="center")

    # notes
    notes_label = tk.Label(second_frame, text="if you want you can write a notes...", font=("Arial", 13, "bold"),
                           foreground="green", anchor="center", justify="center", bg="light blue")

    notes_label.place(relx=0.5, rely=0.26, anchor="center")

    notes_box = tk.Entry(second_frame, width=35)
    notes_box.bind("<Return>", lambda event: submit_data())
    notes_box.place(relx=0.5, rely=0.3, anchor="center")

    # extracting button
    end_button = tk.Button(second_frame, text="extract to file", command=lambda: [export_file()])
    end_button.place(relx=.1, rely=0.95, anchor="center")

    # back button
    back_button = tk.Button(second_frame, text="go back", command=lambda: [change_frame(second_frame, entry_frame)])
    back_button.place(relx=0.05, rely=0.05, anchor="center")

    # labels showtime
    columns = ("time", "subject", "notes")
    tasks = ttk.Treeview(second_frame, columns=columns)

    tasks["show"] = "headings"

    tasks.heading("time", text="task")
    tasks.column("time", width=40)

    tasks.heading("subject", text="subject")
    tasks.column("subject", width=40)

    tasks.heading("notes", text="notes")
    tasks.column("notes", width=40)

    tasks.place(relx=0.5, rely=0.6, anchor="center", width=800, height=300)

    # # time
    # title_time = tk.Label(second_frame, text="time", font=("Arial", 13, "bold"), foreground="orange", anchor="center",
    #                       justify="center", bg="light blue")
    # title_time.place(relx=0.1, rely=0.34, anchor="center")
    #
    # lable_time = tk.Label(second_frame, textvariable=time_saver, font=("Arial", 13), foreground="black",
    #                       anchor="center", justify="center", bg="light blue")
    # lable_time.place(relx=0.08, rely=0.35)
    #
    # # subject
    # title_subject = tk.Label(second_frame, text="subject", font=("Arial", 13, "bold"), foreground="orange",
    #                          anchor="center", justify="center", bg="light blue")
    # title_subject.place(relx=0.23, rely=0.34, anchor="center")
    #
    # lable_subject = tk.Label(second_frame, textvariable=subject_saver, font=("Arial", 13), foreground="black",
    #                          anchor="center", justify="center", bg="light blue")
    # lable_subject.place(relx=0.2, rely=0.35)
    #
    # # notes
    # title_notes = tk.Label(second_frame, text="notes", font=("Arial", 13, "bold"), foreground="orange", anchor="center",
    #                        justify="center", bg="light blue")
    # title_notes.place(relx=0.36, rely=0.34, anchor="center")
    #
    # lable_notes = tk.Label(second_frame, textvariable=notes_saver, font=("Arial", 13), foreground="black",
    #                        anchor="center", justify="center", bg="light blue")
    # lable_notes.place(relx=0.32, rely=0.35)

    # chat frame
    messages_box = tk.Listbox(chat_frame)

    def send_msg():
        client_socket.send(msg_var.get().encode())
        messages_box.insert(tk.END, f"you: {msg_var.get()}")
        msg_var.set("")
        print("message sent")

    messages_box.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.8, relheight=0.8)
    message_entry = tk.Entry(chat_frame, textvariable=msg_var)
    message_entry.bind("<Return>", lambda event: send_msg())
    message_entry.place(relx=0.1, rely=0.95, relwidth=0.8)
    send_button = tk.Button(chat_frame, text="send", command=lambda: send_msg())
    send_button.place(relx=0.8, rely=0.95)

    # back to setting schedule

    button_back_schedule = tk.Button(chat_frame, text="back to schedule",
                                     command=lambda: [change_frame(chat_frame, second_frame)])
    button_back_schedule.place(relx=0.9, rely=0.95, anchor="center")

    receive_from_expert_thread = Thread(target=lambda: receive())
    receive_from_expert_thread.start()

    window.mainloop()


if __name__ == '__main__':
    main()
