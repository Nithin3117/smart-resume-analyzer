import plotly.graph_objects as go


# =====================================================
# ATS GAUGE
# =====================================================

def create_gauge(score):

    fig = go.Figure(go.Indicator(

        mode="gauge+number",

        value=score,

        number={
            'font': {
                'size': 70,
                'color': "white"
            }
        },

        title={
            'text': "Resume Match Score",
            'font': {
                'size': 32,
                'color': "white"
            }
        },

        gauge={

            'axis': {
                'range': [0, 100]
            },

            'bar': {
                'color': "white",
                'thickness': 0.25
            },

            'bgcolor': "#1e1e2f",

            'steps': [

                {
                    'range': [0, 40],
                    'color': "#ff4b5c"
                },

                {
                    'range': [40, 60],
                    'color': "#f7c948"
                },

                {
                    'range': [60, 85],
                    'color': "#66ff99"
                },

                {
                    'range': [85, 100],
                    'color': "#00cc66"
                }
            ]
        }
    ))

    fig.update_layout(

        paper_bgcolor="#1e1e2f",

        font={'color': "white"},

        height=500
    )

    return fig
