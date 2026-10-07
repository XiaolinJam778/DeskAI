from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class MessageInput(QTextEdit):
    send_requested = Signal()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                super().keyPressEvent(event)
            else:
                self.send_requested.emit()
            return

        super().keyPressEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DeskAI")
        self.resize(720, 520)
        self.setMinimumSize(560, 420)

        self._setup_ui()
        self._connect_signals()

        self.input_box.setFocus()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(12)

        title_label = QLabel("DeskAI")

        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)

        main_layout.addWidget(title_label)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setPlaceholderText("AI 的回答会显示在这里")
        main_layout.addWidget(self.chat_display)

        input_label = QLabel("你想问什么？")
        main_layout.addWidget(input_label)

        self.input_box = MessageInput()
        self.input_box.setPlaceholderText(
            "输入你的问题……\nEnter 发送，Shift + Enter 换行"
        )
        self.input_box.setMaximumHeight(110)
        main_layout.addWidget(self.input_box)

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.clear_button = QPushButton("清空")
        self.send_button = QPushButton("发送")

        self.send_button.setDefault(True)

        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.send_button)

        main_layout.addLayout(button_layout)

    def _connect_signals(self):
        self.clear_button.clicked.connect(self.clear_chat)
        self.send_button.clicked.connect(self.send_message)
        self.input_box.send_requested.connect(self.send_message)

    def clear_chat(self):
        self.chat_display.clear()
        self.input_box.clear()
        self.input_box.setFocus()

    def send_message(self):
        message = self.input_box.toPlainText().strip()

        if not message:
            return

        self.chat_display.append(f"你：{message}")
        self.chat_display.append("DeskAI：AI 服务尚未连接。\n")

        self.input_box.clear()
        self.input_box.setFocus()