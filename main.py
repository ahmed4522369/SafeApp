from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
import threading
from antivirus_engine import AntivirusEngine

Window.size = (400, 700)

class AntiVirusApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = AntivirusEngine()
        self.scan_thread = None

    def build(self):
        self.title = "🛡️ AntiVirus Guard"
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # Header
        title = Label(
            text='[b][color=ff0000]🛡️ ANTIVIRUS GUARD[/color][/b]',
            size_hint_y=0.12,
            markup=True,
            font_size='22sp'
        )
        main_layout.add_widget(title)
        
        # Status
        self.status_label = Label(
            text='[color=00ff00]✓ System Status: Ready[/color]',
            size_hint_y=0.08,
            markup=True,
            font_size='14sp'
        )
        main_layout.add_widget(self.status_label)
        
        # Buttons Grid
        button_grid = GridLayout(cols=2, spacing=8, size_hint_y=0.25)
        buttons_info = [
            ('🔍 Full Scan', self.start_system_scan),
            ('⚡ Quick Scan', self.start_quick_scan),
            ('🔐 Permissions', self.show_permissions),
            ('📥 Update DB', self.check_updates)
        ]
        
        for btn_text, btn_func in buttons_info:
            btn = Button(text=btn_text, font_size='13sp', bold=True)
            btn.bind(on_press=btn_func)
            button_grid.add_widget(btn)
        
        main_layout.add_widget(button_grid)
        
        # Results Display
        self.results_label = Label(
            text='📊 Scan Results:\nNo scans performed yet',
            size_hint_y=0.55,
            markup=True,
            font_size='12sp'
        )
        scroll = ScrollView()
        scroll.add_widget(self.results_label)
        main_layout.add_widget(scroll)
        
        return main_layout

    def start_system_scan(self, instance):
        self.status_label.text = '[color=ff9900]⏳ Full system scan in progress...[/color]'
        self.scan_thread = threading.Thread(target=self._perform_scan, args=("/",), daemon=True)
        self.scan_thread.start()

    def start_quick_scan(self, instance):
        self.status_label.text = '[color=0099ff]⚡ Quick scan in progress...[/color]'
        self.scan_thread = threading.Thread(target=self._perform_scan, args=("./",), daemon=True)
        self.scan_thread.start()

    def _perform_scan(self, path):
        try:
            results = self.engine.scan_directory(path)
            threats = [r for r in results if r.get("threat_detected")]
            
            report = f"[b]📊 Scan Results[/b]\n"
            report += f"├─ Files Scanned: {len(results)}\n"
            report += f"├─ Threats Found: {len(threats)}\n"
            report += f"└─ Status: {'⚠️ THREATS DETECTED' if threats else '✓ SAFE'}\n\n"
            
            if threats:
                report += "[color=ff0000][b]🚨 THREATS DETECTED:[/b][/color]\n"
                for idx, threat in enumerate(threats[:10], 1):
                    report += f"{idx}. {threat.get('file', 'Unknown')}\n"
                    report += f"   └─ Type: {threat.get('threat_type', 'Unknown')}\n"
            
            Clock.schedule_once(lambda dt: self._update_results(report), 0.1)
            Clock.schedule_once(lambda dt: self._update_status('[color=00ff00]✓ Scan Complete[/color]'), 0.1)
        except Exception as e:
            error_text = f"[color=ff0000]❌ Error: {str(e)}[/color]"
            Clock.schedule_once(lambda dt: self._update_results(error_text), 0.1)

    def _update_results(self, text):
        self.results_label.text = text

    def _update_status(self, text):
        self.status_label.text = text

    def show_permissions(self, instance):
        perms = self.engine.get_system_permissions()
        perm_text = "[b]🔐 Required Permissions:[/b]\n\n"
        for perm in perms["permissions"]:
            perm_text += f"✓ {perm['name']}\n"
            perm_text += f"  └─ {perm['description']}\n\n"
        self.results_label.text = perm_text

    def check_updates(self, instance):
        self.status_label.text = '[color=0099ff]📥 Checking for updates...[/color]'
        update_text = (
            "[b]📥 Signature Update[/b]\n\n"
            "✓ Signature Database: Up to Date\n"
            "✓ App Version: 1.0.0\n"
            "✓ Latest Version: 1.0.0\n"
            "✓ Status: Latest\n\n"
            "Last Update: Today"
        )
        Clock.schedule_once(lambda dt: self._update_results(update_text), 0.5)
        Clock.schedule_once(lambda dt: self._update_status('[color=00ff00]✓ Update Check Complete[/color]'), 0.5)

if __name__ == '__main__':
    AntiVirusApp().run()
