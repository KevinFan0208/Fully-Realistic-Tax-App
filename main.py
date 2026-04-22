import flet as ft

def main(page: ft.Page):
    page.title = "收入纳税明细"
    page.bgcolor = "#F5F6F8"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    form_rows = []
    cards_ui = []

    # =========================
    # 创建输入卡片 (第一屏逻辑)
    # =========================
    def create_input_card():
        date = ft.TextField(label="日期（如 2025-12）", value="2025-12")
        type_ = ft.TextField(label="所得项目小类", value="正常工资薪金")
        company = ft.TextField(label="扣缴义务人", value="深圳亦创科技有限公司")
        income = ft.TextField(label="收入", value="6811.00")
        tax = ft.TextField(label="已申报税额", value="0.00")

        data_ref = {"date": date, "type": type_, "company": company, "income": income, "tax": tax}

        card = ft.Container(
            bgcolor="white", border_radius=12, padding=15,
            content=ft.Column([date, type_, company, income, tax], spacing=10)
        )
        return card, data_ref

    def show_input_view():
        page.clean()
        form_rows.clear()
        cards_ui.clear()

        card, data = create_input_card()
        form_rows.append(data)
        cards_ui.append(card)

        list_column = ft.Column(cards_ui, spacing=12)

        def add_row(e):
            card, data = create_input_card()
            form_rows.append(data)
            list_column.controls.append(card)
            page.update()

        def generate(e):
            data_list = []
            for r in form_rows:
                if r["date"].value:
                    data_list.append({
                        "date": r["date"].value,
                        "type": r["type"].value,
                        "company": r["company"].value,
                        "income": float(r["income"].value or 0),
                        "tax": float(r["tax"].value or 0),
                    })
            show_display_view(data_list)

        page.add(
            ft.SafeArea(
                content=ft.Column([
                    ft.AppBar(title=ft.Text("信息录入", weight=ft.FontWeight.BOLD), center_title=True, bgcolor="white"),
                    ft.Container(
                        padding=15, expand=True,
                        content=ft.Column([
                            list_column,
                            ft.Button("➕ 添加月份", on_click=add_row),
                            ft.Button("生成预览", on_click=generate)
                        ], scroll=ft.ScrollMode.AUTO)
                    )
                ], expand=True)
            )
        )

    # =========================
    # 第二屏（展示页）
    # =========================
    def show_display_view(data_list):
        page.clean()
        total_income = sum(d["income"] for d in data_list)
        total_tax = sum(d["tax"] for d in data_list)

        def go_back(e):
            show_input_view()

        page.add(
            ft.SafeArea(
                content=ft.Column([
                    # 顶部导航栏
                    ft.Container(
                        bgcolor="white",
                        padding=ft.padding.only(left=10, right=15, top=15, bottom=15),
                        content=ft.Row([
                            ft.GestureDetector(
                                on_tap=go_back,
                                content=ft.Row([
                                    ft.Icon(ft.Icons.ARROW_BACK_IOS_NEW, size=18, color="#007AFF"),
                                    ft.Text("返回", color="#007AFF", size=16)
                                ], spacing=2)
                            ),
                            ft.Text("收入纳税明细", size=17, weight=ft.FontWeight.W_500),
                            ft.Text("批量申诉", color="#007AFF", size=15),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ),
                    # 内容区
                    ft.Column([
                        # 汇总模块
                        ft.Container(
                            bgcolor="white",
                            padding=ft.padding.only(left=15, right=15, top=20, bottom=20),
                            content=ft.Column([
                                summary_row("收入合计", total_income, True),
                                ft.Divider(height=1, color="#EEEEEE"),
                                summary_row("已申报税额合计", total_tax, False),
                            ], spacing=15)
                        ),
                        # 列表模块
                        ft.Column(
                            [income_card(d) for d in data_list],
                            spacing=10
                        )
                    ], scroll=ft.ScrollMode.AUTO, expand=True)
                ], expand=True)
            )
        )

    # 单条卡片 UI
    def income_card(d):
        return ft.Container(
            bgcolor="white",
            padding=15,
            content=ft.Column([
                ft.Row([
                    ft.Text("工资薪金", size=16, color="#333333"),
                    ft.Text(d["date"], size=16, color="#333333"),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=2),
                build_row("所得项目小类", d["type"]),
                build_row("扣缴义务人", d["company"], True),
                build_row("收入", f"{d['income']:,.2f}元"),
                build_row("已申报税额", f"{d['tax']:,.2f}元"),
            ], spacing=6)
        )

    # 明细行 UI
    def build_row(label, value, arrow=False):
        return ft.Row([
            ft.Text(f"{label}：", color="#999999", size=14),
            ft.Text(value, color="#777777", size=14),
            ft.Container(expand=True),
            ft.Icon(ft.Icons.CHEVRON_RIGHT, size=18, color="#D1D1D1") if arrow else ft.Container(),
        ], spacing=0)

    # 汇总行 UI
    def summary_row(label, value, show_icon):
        return ft.Row([
            ft.Text(label, color="#333333", size=15),
            ft.Container(width=5),
            ft.Container(
                content=ft.Row(
                    [ft.Text("?", color="#007AFF", size=11, weight=ft.FontWeight.BOLD)],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                border=ft.border.all(1, "#007AFF"),
                border_radius=8,
                width=16, height=16,
            ) if show_icon else ft.Container(),
            ft.Container(expand=True),
            ft.Text(f"{value:,.2f}元", color="#333333", size=16),
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER)

    show_input_view()

ft.run(main)
