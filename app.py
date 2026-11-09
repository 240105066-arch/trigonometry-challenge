import streamlit as st
import time
import streamlit.components.v1 as components

st.set_page_config(page_title='Trigonometry Challenge', page_icon='📐', layout='wide', initial_sidebar_state='collapsed')

QUESTIONS = [
    dict(q=r'Find the exact value of $\sin 30^\circ+\cos 60^\circ$.', opts=[r'$\frac12$',r'$1$',r'$\frac{\sqrt3}{2}$',r'$2$'], ans=1, hints=['Recall the special-angle values for 30° and 60°.','Both terms equal one half. Add them.'], solution=r'$\sin30^\circ+\cos60^\circ=\frac12+\frac12=1$'),
    dict(q=r'How many solutions does $\sin x=\frac12$ have for $0^\circ\leq x<360^\circ$?',opts=['0','1','2','4'],ans=2,hints=['Use the unit circle: sine is positive in quadrants I and II.','The reference angle is 30°. Find the angles in quadrants I and II.'],solution=r'$x=30^\circ,150^\circ$, so there are 2 solutions.'),
    dict(q=r'If $\sin x=\frac35$ and $x$ is in Quadrant I, find $\tan x$.',opts=[r'$\frac34$',r'$\frac43$',r'$\frac35$',r'$\frac45$'],ans=0,hints=[r'Use $\sin^2x+\cos^2x=1$ and $\tan x=\frac{\sin x}{\cos x}$.',r'In Quadrant I, $\cos x=\frac45$. Divide $\frac35$ by $\frac45$.'],solution=r'$\cos x=\frac45$, hence $\tan x=\frac{3/5}{4/5}=\frac34$.'),
    dict(q=r'Solve $2\cos x-1=0$ for $0\leq x<2\pi$.',opts=[r'$\frac\pi6,\frac{11\pi}6$',r'$\frac\pi3,\frac{2\pi}3$',r'$\frac{2\pi}3,\frac{4\pi}3$',r'$\frac\pi3,\frac{5\pi}3$'],ans=3,hints=[r'First isolate $\cos x$. Think about where cosine is positive.',r'$\cos x=\frac12$; use quadrants I and IV.'],solution=r'$\cos x=\frac12\Rightarrow x=\frac\pi3,\frac{5\pi}3$.'),
    dict(q=r'If $\sin x=\frac35$ and $x$ is in Quadrant II, find $\cos x$.',opts=[r'$\frac45$',r'$-\frac45$',r'$-\frac35$',r'$\frac25$'],ans=1,hints=[r'Use $\sin^2x+\cos^2x=1$.',r'$|\cos x|=\frac45$, but cosine is negative in Quadrant II.'],solution=r'$\cos^2x=1-\frac9{25}=\frac{16}{25}$; in Quadrant II, $\cos x=-\frac45$.'),
    dict(q=r'What is the sum of all solutions of $\sin 2x=0$ for $0\leq x<2\pi$?',opts=[r'$\pi$',r'$2\pi$',r'$3\pi$',r'$4\pi$'],ans=2,hints=[r'For $\sin\theta=0$, $\theta=k\pi$.',r'Set $2x=k\pi$. List $x=0,\frac\pi2,\pi,\frac{3\pi}2$ and add.'],solution=r'$x=0,\frac\pi2,\pi,\frac{3\pi}2$; sum $=3\pi$.'),
    dict(q=r'How many distinct solutions does $2\sin^2x-3\sin x+1=0$ have for $0\leq x<2\pi$?',opts=['1','2','3','4'],ans=2,hints=[r'Treat $\sin x$ as a variable and factor the quadratic.',r'$(2\sin x-1)(\sin x-1)=0$. Count solutions of both sine equations.'],solution=r'$\sin x=\frac12$ gives 2 solutions; $\sin x=1$ gives 1. Total: 3.'),
    dict(q=r'Solve $\sin x+\cos x=1$ for $0\leq x<2\pi$.',opts=[r'$0,\frac\pi2$',r'$\frac\pi4,\frac{5\pi}4$',r'$0,\pi$',r'$\frac\pi2,\pi$'],ans=0,hints=[r'Square both sides and use $\sin^2x+\cos^2x=1$. Check answers in the original equation.',r'Squaring gives $\sin2x=0$. Of the four candidates, only two satisfy the original equation.'],solution=r'Squaring yields $\sin2x=0$, so candidates are $0,\frac\pi2,\pi,\frac{3\pi}2$. Checking gives $0,\frac\pi2$.'),
    dict(q=r'What is the sum of all distinct solutions of $\cos2x=\sin x$ for $0\leq x<2\pi$?',opts=[r'$2\pi$',r'$\frac{5\pi}2$',r'$3\pi$',r'$\frac{7\pi}2$'],ans=1,hints=[r'Rewrite $\cos2x$ using $\sin x$: $\cos2x=1-2\sin^2x$.',r'Factor $(2\sin x-1)(\sin x+1)=0$. Find the three angles and sum them.'],solution=r'$x=\frac\pi6,\frac{5\pi}6,\frac{3\pi}2$; sum $=\frac{5\pi}2$.'),
    dict(q=r'What is the sum of all distinct solutions of $\sin3x=\cos x$ for $0\leq x<2\pi$?',opts=[r'$5\pi$',r'$\frac{11\pi}2$',r'$6\pi$',r'$\frac{13\pi}2$'],ans=0,hints=[r'Use $\cos x=\sin(\frac\pi2-x)$ and the two cases for equal sines.',r'The solution families are $x=\frac\pi8+\frac{k\pi}2$ and $x=\frac\pi4+k\pi$. List all angles in the interval.'],solution=r'The six angles are $\frac\pi8,\frac{5\pi}8,\frac{9\pi}8,\frac{13\pi}8,\frac\pi4,\frac{5\pi}4$. Their sum is $5\pi$.'),
]

# Targeted, pre-reviewed feedback for each possible incorrect question.
# The final message is assembled from the exact set of incorrect answers.
QUESTION_FEEDBACK = [
    "Review special-angle sine and cosine values (30° and 60°). Use the unit circle or a special-angle table, then practise evaluating short expressions.",
    "Review how many angles can have the same sine value on a full turn. Practise identifying the reference angle and checking both relevant quadrants.",
    "Review the Pythagorean identity and the tangent ratio. Find cosine from a given sine value, choose its sign from the quadrant, then divide sine by cosine.",
    "Review solving basic cosine equations on [0, 2π). Isolate cosine, identify its reference angle, and include every valid quadrant before listing solutions.",
    "Review the signs of sine and cosine in each quadrant. Use sin²x + cos²x = 1 to find the magnitude, then select the correct sign in Quadrant II.",
    "Review equations with double angles. For sin(2x) = 0, list every value of x in the specified interval before adding them; avoid missing endpoints or extra roots.",
    "Review factoring quadratic expressions in sin(x). Solve each resulting sine equation separately and count distinct angles, including special cases such as sin(x) = 1.",
    "Review trigonometric equations that require checking solutions. Squaring can introduce extraneous answers, so substitute each candidate back into the original equation.",
    "Review the double-angle identity cos(2x) = 1 − 2sin²(x). Factor the resulting equation, find all distinct angles, and add them carefully.",
    "Review equations involving different angle multiples. Convert cosine to sine, solve both sine-equation families, then list and sum every solution in [0, 2π).",
]

def feedback_for_results():
    unanswered = [i for i in range(10) if i not in (s.submitted if s.feedback_mode == 'At the end' else s.solved)]
    if len(unanswered) > 7:
        return ("Start with the fundamentals", "You completed fewer than three questions. A reliable topic-by-topic assessment is not possible yet. Review the full trigonometry unit, beginning with special angles, the unit circle, trigonometric identities, and solving equations. Then retake all ten questions to identify your specific strengths and gaps.")
    if s.feedback_mode == 'At the end':
        wrong = [i for i in range(10) if i in s.submitted and s.selections.get(i) != QUESTIONS[i]['ans']]
    else:
        # In Instant mode, a wrong attempt reveals a learning gap even if the student later solves the item.
        wrong = [i for i in range(10) if s.mistakes.get(i, 0) > 0]
    if not wrong and not unanswered:
        return ("Excellent work!", "You answered all ten questions correctly" + (" without incorrect attempts." if s.feedback_mode == 'Instant' else ".") + " You demonstrated a strong grasp of special angles, identities, trigonometric equations, and solution counting. For a next challenge, solve similar problems without multiple-choice options.")
    if not wrong:
        return ("Good progress", "You have no recorded incorrect answers. Complete the remaining questions to receive a full assessment of your trigonometry skills.")
    intro = ("You made incorrect attempts on" if s.feedback_mode == 'Instant' else "You answered incorrectly on") + " question" + ("s" if len(wrong) != 1 else "") + " " + ", ".join(str(i+1) for i in wrong) + ". Focus on these specific areas:"
    lines = [f"**Question {i+1}:** {QUESTION_FEEDBACK[i]}" for i in wrong]
    if unanswered:
        lines.append("**Unanswered:** Complete questions " + ", ".join(str(i+1) for i in unanswered) + " to get a fuller assessment.")
    return ("Your personalised study feedback", intro + "\n\n" + "\n\n".join(lines))

LEVELS = [('EASY',0,3),('MEDIUM',3,7),('HARD',7,10)]
DEFAULTS = dict(page='home', current=0, solved=set(), mistakes={}, selections={}, hint_open=False, theme='Light', timer_minutes=15, started_at=None, expired=False, feedback_mode='Instant', submitted=set())
for k,v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v.copy() if isinstance(v,(dict,set)) else v

s=st.session_state
DARK=s.theme=='Dark'
BG='#081f27' if DARK else '#70c4b5'
FG='#edf8f5' if DARK else '#193a36'
CARD='#1c3c48' if DARK else '#ffffff'
BORDER='#456c77' if DARK else '#d6eae6'
MUTED='#b9d5dc' if DARK else '#527a74'
GREEN='#15885f'

st.markdown(f'''<style>
:root {{color-scheme:{'dark' if DARK else 'light'};}}
.stApp,[data-testid="stAppViewContainer"] {{background:{BG}!important;color:{FG}!important;}}
[data-testid="stHeader"] {{background:transparent!important;}}
[data-testid="stSidebar"] {{background:{BG}!important;}}
[data-testid="stSidebar"] > div:first-child {{background:{CARD}!important;margin:10px;border-radius:24px;min-height:calc(100vh - 20px);box-shadow:0 12px 35px #001b1c24;}}
[data-testid="stSidebar"] * {{color:{FG}!important;}}
.block-container {{max-width:1370px;padding-top:1.3rem;padding-bottom:3rem;}}
h1,h2,h3,h4,p,label {{color:{FG};}}
.st-key-header_island,.st-key-home_island,.st-key-progress_island,.st-key-navigation_island,.st-key-question_island,.st-key-hint_island,.st-key-results_island,.st-key-result_stat {{
 background:{CARD}!important;border:1px solid {BORDER}!important;border-radius:24px!important;
 box-shadow:0 14px 32px #062e3226!important;padding:20px!important;
}}
.st-key-home_island {{padding:42px!important;}}
.st-key-header_island {{padding:12px 22px!important;margin-bottom:18px;}}
.st-key-navigation_island,.st-key-question_island {{min-height:430px;}}
.st-key-result_stat {{min-height:115px;}}
.st-key-home_island [data-testid="stVerticalBlockBorderWrapper"],
.st-key-navigation_island [data-testid="stVerticalBlockBorderWrapper"] {{
 background:transparent!important;
}}
[data-testid="stVerticalBlockBorderWrapper"] {{
 background:{CARD}!important;border-color:{BORDER}!important;border-radius:20px!important;
}}
.st-key-home_island .st-key-level_easy,.st-key-home_island .st-key-level_medium,.st-key-home_island .st-key-level_hard {{
 background:{'rgba(255,255,255,.065)' if DARK else '#f1f9f7'}!important;
 border:1px solid {BORDER}!important;border-radius:18px;padding:16px;
}}
.stButton > button {{
 background:{CARD}!important;color:{FG}!important;border:1.5px solid {GREEN}!important;
 border-radius:12px!important;min-height:45px;font-weight:600;
 transition:background .18s,color .18s,transform .18s!important;
}}
.stButton > button:hover {{background:{GREEN}!important;color:white!important;transform:translateY(-1px);}}
.stButton > button[kind="primary"] {{background:{GREEN}!important;color:white!important;}}
.stButton > button:disabled {{opacity:.42!important;transform:none!important;}}
[data-testid="stRadio"] label {{background:{'rgba(255,255,255,.08)' if DARK else '#f5faf8'}!important;
 border:1px solid {BORDER}!important;border-radius:12px;padding:10px!important;margin:3px 0;}}
[data-testid="stRadio"] label:hover {{border-color:{GREEN}!important;}}
[data-testid="stProgress"] > div > div > div {{background:{GREEN}!important;}}
[data-testid="stMetric"] {{background:{CARD};border:1px solid {BORDER};border-radius:18px;padding:15px;}}
[data-testid="stExpander"] {{background:{CARD}!important;border:1px solid {BORDER}!important;border-radius:14px!important;margin-bottom:9px;}}
[data-testid="stAlert"] {{border-radius:13px;}}
 [data-testid="stAlert"] {{background:#e9f7f2!important;border:1px solid #a2d8c7!important;}}
 [data-testid="stAlert"] *,[data-testid="stAlert"] p {{color:#143f35!important;}}
 [data-testid="stExpander"] details summary,[data-testid="stExpander"] details summary * {{color:{FG}!important;background:{CARD}!important;}}
 [data-testid="stExpander"] details[open] summary {{border-bottom:1px solid {BORDER}!important;}}
.quiz-tag {{display:inline-block;border:1px solid {GREEN};border-radius:30px;padding:7px 14px;color:{GREEN};font-weight:750;font-size:12px;letter-spacing:.7px;}}
.hero-island {{text-align:center;padding:24px 8px 28px;}}
.hero-island h1 {{color:{FG};font-size:clamp(36px,4.8vw,64px);letter-spacing:-2px;margin:18px 0;}}
.hero-island p {{color:{MUTED};font-size:18px;line-height:1.7;}}
.small-muted {{color:{MUTED};font-size:14px;}}
</style>''',unsafe_allow_html=True)

def live_timer():
    if not s.timer_minutes or not s.started_at:
        return
    deadline_ms=int((s.started_at+s.timer_minutes*60)*1000)
    fg='#e9fff6' if DARK else '#173d35'
    bg='#173735' if DARK else '#ffffff'
    components.html(f'''<!doctype html><html><head><style>
    body{{margin:0;background:transparent;font-family:Arial,sans-serif;}}
    .timer{{display:flex;align-items:center;gap:13px;background:{bg};color:{fg};border:1px solid #15885f55;border-radius:17px;padding:11px 16px;width:max-content;box-sizing:border-box;}}
    .dial{{width:35px;height:35px;border:3px solid #15885f;border-radius:50%;display:grid;place-items:center;font-size:19px;color:#15885f;}}
    .sub{{font-size:10px;letter-spacing:1.2px;opacity:.7;font-weight:700;}}
    #clock{{font-size:25px;font-weight:800;letter-spacing:1px;font-variant-numeric:tabular-nums;}}
    </style></head><body><div class="timer"><div class="dial">◷</div><div><div class="sub">TIME LEFT</div><div id="clock">--:--</div></div></div>
    <script>
    const end={deadline_ms};let announced=false;
    function tick(){{let t=Math.max(0,Math.ceil((end-Date.now())/1000));document.getElementById('clock').textContent=String(Math.floor(t/60)).padStart(2,'0')+':'+String(t%60).padStart(2,'0');if(t===0&&!announced){{announced=true;document.getElementById('clock').style.color='#e05757';}}}}
    tick();setInterval(tick,250);
    </script></body></html>''',height=76)

def level_of(i):
    return 0 if i<3 else 1 if i<7 else 2

def unlocked(level):
    return level==0 or all(i in (s.solved if s.feedback_mode=='Instant' else s.submitted) for i in range(LEVELS[level-1][1],LEVELS[level-1][2]))

def begin():
    s.page='quiz';s.current=0;s.solved=set();s.mistakes={};s.selections={};s.submitted=set();s.hint_open=False;s.started_at=time.time();s.expired=False

def move(i):
    s.current=i;s.hint_open=False

@st.fragment(run_every="1s")
def countdown():
    if s.timer_minutes and s.started_at:
        remaining=max(0,int(s.timer_minutes*60-(time.time()-s.started_at)))
        if remaining<=0:
            s.expired=True;s.page='results'
            st.rerun()
        live_timer()

with st.sidebar:
    st.header('⚙️ Settings')
    dark_switch=st.toggle('🌙 Dark mode',value=DARK,key='dark_mode_switch')
    if dark_switch!=DARK:
        s.theme='Dark' if dark_switch else 'Light'
        st.rerun()
    st.divider()
    st.markdown('### ⏱️ Quiz timer')
    if s.page=='home':
        st.caption('Choose the time before you start. The clock will count down continuously.')
        enabled=st.toggle('Enable timer',value=s.timer_minutes>0,key='timer_enabled')
        if enabled:
            chosen=st.slider('Minutes',min_value=1,max_value=60,value=min(60,max(1,s.timer_minutes)),step=1,format='%d min')
            s.timer_minutes=chosen
        else:
            s.timer_minutes=0
            chosen=0
            st.caption('Unlimited time — no countdown.')
        st.markdown(f'<div style="border:2px solid {GREEN};border-radius:50%;width:105px;height:105px;margin:14px auto;display:flex;align-items:center;justify-content:center;background:{CARD};font-size:23px;font-weight:800;color:{GREEN};">{chosen if chosen else "∞"}<span style="font-size:11px;margin-left:4px">{"min" if chosen else ""}</span></div>',unsafe_allow_html=True)
    else:
        st.info('Timer: '+(f'{s.timer_minutes} minutes' if s.timer_minutes else 'Off')+' · Restart to change duration.')
    st.divider()
    st.markdown('### 🎯 Answer feedback')
    feedback_choice=st.radio('When should answers be checked?', ['Instant','At the end'], index=0 if s.feedback_mode=='Instant' else 1, disabled=s.page!='home', help='Instant: retry incorrect answers and unlock levels by solving them. At the end: submit one answer per question, see correctness only on the results page.')
    s.feedback_mode=feedback_choice
    if s.page!='home': st.caption('Restart from Home to change feedback mode.')
    st.divider()
    st.subheader('About')
    st.write('An interactive 10-question trigonometry quiz with progressive hints.')
    st.caption('Author contact: to be added.')
    if s.page!='home' and st.button('⌂ Home',use_container_width=True):
        s.page='home';st.rerun()

with st.container(key='header_island'):
    st.markdown(f'<b style="color:{FG}">◉ TRIGONOMETRY CHALLENGE</b>',unsafe_allow_html=True)

if s.page=='home':
    with st.container(key='home_island'):
        st.markdown('<div class="hero-island"><span class="quiz-tag">MATHEMATICS · 10 QUESTIONS</span><h1>Think. Solve. Improve.</h1><p>Master trigonometry one question at a time.<br>Three levels. Helpful hints. Your own pace.</p></div>',unsafe_allow_html=True)
        a,b,c=st.columns([2,1.4,2])
        with b:
            if st.button('Start Quiz →',type='primary',use_container_width=True):
                begin();st.rerun()
        st.write('')
        x,y,z=st.columns(3)
        for col,(name,desc) in zip([x,y,z],[('01 · EASY','3 questions'),('02 · MEDIUM','4 questions'),('03 · HARD','3 questions')]):
            with col:
                with st.container(key='level_'+name.split('·')[-1].strip().lower()):
                    st.subheader(name);st.caption(desc)
        st.caption('Set the timer in the left sidebar before starting. You can switch themes at any time.')

elif s.page=='quiz':
    countdown()
    progress_count=len(s.solved if s.feedback_mode=='Instant' else s.submitted)
    with st.container(key='progress_island'):
        st.progress(progress_count/10,text=f'{progress_count} of 10 questions '+('solved' if s.feedback_mode=='Instant' else 'submitted'))
    nav,main=st.columns([1,3.5],gap='large')
    with nav:
        with st.container(key='navigation_island'):
            st.markdown('#### Questions')
            for level,(name,start,end) in enumerate(LEVELS):
                can=unlocked(level)
                st.markdown(f'**{name}** '+('' if can else '🔒'))
                cols=st.columns(end-start)
                for idx,col in zip(range(start,end),cols):
                    with col:
                        symbol='✓' if idx in (s.solved if s.feedback_mode=='Instant' else s.submitted) else ('●' if idx==s.current else str(idx+1))
                        if st.button(symbol,key=f'nav_{idx}',disabled=not can,use_container_width=True):
                            move(idx);st.rerun()
                st.write('')
        st.caption('Complete every question in a level to unlock the next one.')
    with main:
        idx=s.current
        if not unlocked(level_of(idx)):
            s.current=0
            st.rerun()
        q=QUESTIONS[idx]
        level=level_of(idx)
        errors=s.mistakes.get(idx,0)
        can_hint=s.feedback_mode=='Instant' and errors>=1 and idx not in s.solved
        show_hint=can_hint and s.hint_open
        if show_hint:
            question_col,hint_col=st.columns([1.65,1],gap='medium')
        else:
            question_col=st.container()
            hint_col=None
        with question_col:
            with st.container(key='question_island'):
                st.markdown(f'<span class="quiz-tag">{LEVELS[level][0]} · QUESTION {idx+1}/10</span>',unsafe_allow_html=True)
                st.write('')
                st.markdown(f'### {q["q"]}')
                st.write('')
                labels=[f'{chr(65+i)})  {opt}' for i,opt in enumerate(q['opts'])]
                selected=st.radio('Choose your answer:',options=list(range(4)),format_func=lambda j:labels[j],index=None if idx not in s.selections else s.selections[idx],key=f'answer_{idx}',disabled=idx in (s.solved if s.feedback_mode=='Instant' else s.submitted))
                if idx in s.submitted and s.feedback_mode=='At the end':
                    st.info('Answer saved. Correctness will be revealed on the results page.')
                elif idx in s.solved:
                    st.success('Correct! This question is complete.')
                else:
                    if errors and s.feedback_mode=='Instant':
                        st.error(f'Not quite. Attempts with incorrect answers: {errors}. Try again!')
                    action,hint_action=st.columns([2,1])
                    with action:
                        if st.button('Submit Answer' if s.feedback_mode=='At the end' else 'Check Answer',type='primary',use_container_width=True,disabled=selected is None or (s.feedback_mode=='At the end' and idx in s.submitted),key=f'check_{idx}'):
                            s.selections[idx]=selected
                            if s.feedback_mode=='At the end':
                                s.submitted.add(idx)
                            elif selected==q['ans']:
                                s.solved.add(idx);s.hint_open=False
                            else:
                                s.mistakes[idx]=errors+1
                            st.rerun()
                    with hint_action:
                        if can_hint:
                            hint_number=2 if errors>=2 and level>0 else 1
                            if st.button(f'💡 Hint {hint_number}',use_container_width=True,key=f'hint_{idx}'):
                                s.hint_open=not s.hint_open;st.rerun()
                if idx in s.solved and s.feedback_mode=='Instant':
                    st.markdown('**Explanation**')
                    st.markdown(q['solution'])
        if show_hint and hint_col is not None:
            with hint_col:
                with st.container(key='hint_island'):
                    top1,top2=st.columns([4,1])
                    with top1:st.markdown('### 💡 Hint')
                    with top2:
                        if st.button('✕',key=f'close_hint_{idx}'):
                            s.hint_open=False;st.rerun()
                    hint_number=1 if level==0 or errors==1 else 2
                    st.caption(f'Hint {hint_number} · tailored to this question')
                    st.markdown(q['hints'][hint_number-1])
                    if hint_number==2:
                        st.caption('You can still solve it yourself!')
        st.write('')
        prev_col,next_col=st.columns(2)
        start,end=LEVELS[level][1],LEVELS[level][2]
        with prev_col:
            if st.button('← Previous',disabled=idx<=start,use_container_width=True):
                move(idx-1);st.rerun()
        with next_col:
            if idx<end-1:
                if st.button('Next →',use_container_width=True):
                    move(idx+1);st.rerun()
            elif level<2:
                if unlocked(level+1):
                    if st.button('Next Level →',type='primary',use_container_width=True):
                        move(LEVELS[level+1][1]);st.rerun()
                else:
                    st.button('🔒 Complete this level',disabled=True,use_container_width=True)
            elif len(s.solved if s.feedback_mode=='Instant' else s.submitted)==10:
                if st.button('See Results →',type='primary',use_container_width=True):
                    s.page='results';st.rerun()
            else:
                st.button('Finish all Hard questions',disabled=True,use_container_width=True)
        if len(s.solved if s.feedback_mode=='Instant' else s.submitted)==10:
            if st.button('🏆 View Results',use_container_width=True):
                s.page='results';st.rerun()

elif s.page=='results':
    with st.container(key='results_island'):
        st.markdown('## 🏆 Quiz Results')
        st.caption('Your performance and detailed solutions')
    if s.feedback_mode=='At the end':
        correct=sum(s.selections.get(i)==q['ans'] for i,q in enumerate(QUESTIONS) if i in s.submitted)
        if not s.expired:
            st.success(f'You answered {correct} of 10 questions correctly.')
        else:
            st.warning('Time is up. Here are your results so far.')
        c1,c2,c3=st.columns(3)
        c1.metric('Correct',f'{correct}/10')
        c2.metric('Incorrect',sum(s.selections.get(i)!=q['ans'] for i,q in enumerate(QUESTIONS) if i in s.submitted))
        c3.metric('Answered',f'{len(s.submitted)}/10')
        fb_title, fb_body = feedback_for_results()
        with st.container(key='question_island'):
            st.markdown('### 🎯 ' + fb_title)
            st.markdown(fb_body)
        st.markdown('### Review your answers')
        for i,q in enumerate(QUESTIONS):
            with st.expander(f'Question {i+1} · '+('Correct ✓' if i in s.submitted and s.selections.get(i)==q['ans'] else 'Incorrect ✗' if i in s.submitted else 'Not answered')):
                st.markdown(q['q'])
                if i in s.submitted: st.markdown(f'**Your answer:** {chr(65+s.selections[i])} — {q["opts"][s.selections[i]]}')
                st.markdown(f'**Correct answer:** {chr(65+q["ans"])} — {q["opts"][q["ans"]]}')
                st.markdown(q['solution'])
        if st.button('Restart Quiz',type='primary',key='restart_deferred'):
            begin();st.rerun()
        st.stop()
    if s.expired:
        st.warning('Time is up. Here is your progress so far.')
    else:
        st.success('Congratulations! You completed the quiz.')
    c1,c2,c3=st.columns(3)
    c1.metric('Solved',f'{len(s.solved)}/10')
    c2.metric('Incorrect attempts',sum(s.mistakes.values()))
    c3.metric('Accuracy (first attempt)',f'{sum(1 for i in s.solved if s.mistakes.get(i,0)==0)}/10')
    fb_title, fb_body = feedback_for_results()
    with st.container(key='question_island'):
        st.markdown('### 🎯 ' + fb_title)
        st.markdown(fb_body)
    st.markdown('### Answer key and explanations')
    for i,q in enumerate(QUESTIONS):
        with st.expander(f'Question {i+1} · {"Solved" if i in s.solved else "Not solved"}'):
            st.markdown(q['q'])
            st.markdown(f'**Correct answer: {chr(65+q["ans"])} — {q["opts"][q["ans"]]}**')
            st.markdown(q['solution'])
    if st.button('Restart Quiz',type='primary'):
        begin();st.rerun()
