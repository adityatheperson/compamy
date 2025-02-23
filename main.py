from nicegui import ui

ui.upload(on_upload=lambda e: ui.notify(f' {e.name}')).classes('max-w-full')

ui.run()