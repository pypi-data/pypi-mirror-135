from typing import Optional

import urwid


class ChatListContainer(urwid.WidgetPlaceholder):
    def __init__(self, root, chatlist_widget) -> None:
        self.root = root
        self.keymap = root.keymap
        super().__init__(chatlist_widget)

    def keypress(self, size, key: str) -> Optional[str]:
        if key == self.keymap["right"]:
            self.root.main_columns.focus_position = 2
            self.root.right_side.focus_position = 1
        if key == self.keymap["toggle_chatlist"]:
            self.root.main_columns.focus_position = 2
            self.root.right_side.focus_position = 1
            return super().keypress(size, key)
        return super().keypress(size, key)


class MessagesContainer(urwid.WidgetPlaceholder):
    def __init__(self, root, msgs_widget) -> None:
        self.root = root
        self.keymap = root.keymap
        super().__init__(msgs_widget)

    def keypress(self, size, key: str) -> Optional[str]:
        if key == self.keymap["left"]:
            self.root.main_columns.focus_position = 0
        else:
            return super().keypress(size, key)
        return None


class MessageSendContainer(urwid.WidgetPlaceholder):
    def __init__(self, root, msg_send_widget) -> None:
        self.root = root
        self.keymap = root.keymap
        self.msg_send_widget = msg_send_widget
        super().__init__(msg_send_widget)

    def keypress(self, size, key: str) -> Optional[str]:
        key = super().keypress(size, key)
        # send message
        if key == self.keymap["send_msg"]:
            edit = self.msg_send_widget.widgetEdit
            text = edit.get_edit_text().strip()
            if not text:
                return None
            if text.startswith("//"):
                text = text[1:]
            elif text.startswith("/"):
                text = self.process_command(text)
                if text is not None:
                    edit.set_edit_text(text)
                self.resize_zone(size)
                return None
            current_chat = self.root.account.current_chat
            if current_chat.is_contact_request():
                # accept contact requests automatically until UI allows to accept/block
                current_chat.accept()
            current_chat.send_text(text)
            edit.set_edit_text("")
            self.resize_zone(size)
        # give the focus to the chat list
        elif key == self.keymap["left"]:
            self.root.main_columns.focus_position = 0
        # give the focus to the message list
        elif key in ("up", "page up", "esc"):
            self.root.right_side.focus_position = 0
        elif key == self.keymap["reply"]:
            current_chat = self.root.account.current_chat
            if not current_chat:
                return None
            msgs = current_chat.get_messages()
            if not msgs:
                return None
            edit = self.msg_send_widget.widgetEdit
            sender = msgs[-1].get_sender_contact().display_name
            text = msgs[-1].text.strip()
            if not msgs[-1].is_text():
                text = "[File]\n" + text
            reply = f"\n> @{sender}:\n"
            for line in text.splitlines(keepends=True):
                reply += "> " + line
            edit.set_edit_text(reply + "\n\n")
            self.root.main_columns.focus_position = 2
            self.root.right_side.focus_position = 1
            self.resize_zone(size)
        else:
            self.resize_zone(size)
            return key
        return None

    def resize_zone(self, size) -> None:
        text_caption = self.msg_send_widget.text_caption
        text = self.msg_send_widget.widgetEdit.get_edit_text()
        rows_needed = 1
        for line in text.split("\n"):
            rows_needed += int((len(line) + len(text_caption)) / size[0]) + 1
        rows_needed = min(rows_needed, 10)
        contents = self.root.right_side.contents
        if rows_needed != size[1]:
            contents[1] = (contents[1][0], ("given", rows_needed))

    def process_command(self, cmd) -> Optional[str]:
        model = self.root.account
        acc = model.account
        args = cmd.split(maxsplit=1)
        if args[0] == "/query":
            self.msg_send_widget.widgetEdit.set_edit_text("")
            chat = acc.create_chat(args[1].strip())
            model.select_chat_by_id(chat.id)
            return None
        if args[0] == "/join":
            self.msg_send_widget.widgetEdit.set_edit_text("")
            chat = acc.create_group_chat(args[1].strip())
            model.select_chat_by_id(chat.id)
            return None
        if args[0] == "/delete":
            self.msg_send_widget.widgetEdit.set_edit_text("")
            model.current_chat.delete()
            model.select_chat(None)
            return None
        if args[0] == "/names":
            return "\n".join(c.addr for c in model.current_chat.get_contacts())
        if args[0] == "/add":
            for addr in args[1].split(","):
                model.current_chat.add_contact(addr.strip())
        elif args[0] == "/kick":
            for addr in args[1].split(","):
                model.current_chat.remove_contact(addr.strip())
        elif args[0] == "/part":
            model.current_chat.remove_contact(acc.get_self_contact())
        return f"ERROR: Unknown command {args[0]}"
