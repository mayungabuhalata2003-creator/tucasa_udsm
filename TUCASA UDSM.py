from pathlib import Path
import os

import pandas as pd
import streamlit as st


DATA_FILE = Path(__file__).with_name("tucasa_students.csv")
EVENTS_FILE = Path(__file__).with_name("tucasa_events.csv")
CHOIR_EVENTS_FILE = Path(__file__).with_name("tucasa_choir_events.csv")
CHOIR_SONGS_FILE = Path(__file__).with_name("tucasa_choir_songs.csv")
CHOIR_SONGS_DIR = Path(__file__).with_name("choir_song_pdfs")
LEADERS_FILE = Path(__file__).with_name("tucasa_leaders.csv")
LEADERS_PHOTOS_DIR = Path(__file__).with_name("leader_photos")
BRANDING_DIR = Path(__file__).with_name("branding_assets")
BRANDING_FILE = Path(__file__).with_name("tucasa_branding.csv")
QUESTIONS_FILE = Path(__file__).with_name("tucasa_questions.csv")
WHATSAPP_GROUP_URL = "https://chat.whatsapp.com/REPLACE_WITH_TUCASA_GROUP_LINK"
ADMIN_USERNAME = os.getenv("TUCASA_ADMIN_USERNAME", "tucasa_admin")
ADMIN_PASSWORD = os.getenv("TUCASA_ADMIN_PASSWORD", "Tucasa@Mabibo2026!")
CHOIR_ADMIN_USERNAME = os.getenv("TUCASA_CHOIR_ADMIN_USERNAME", "tucasa_choir")
CHOIR_ADMIN_PASSWORD = os.getenv("TUCASA_CHOIR_ADMIN_PASSWORD", "Choir@Mabibo2026!")

st.set_page_config(page_title="TUCASA UDSM MABIBO HOSTEL", page_icon="🎓", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Playfair+Display:wght@600;700&display=swap');
:root { --navy:#102a43; --gold:#d89b32; --cream:#f7f3ea; --ink:#19324d; }
.stApp { background:var(--cream); color:var(--ink); }
[data-testid="stSidebar"] { background:var(--navy); }
[data-testid="stSidebar"] * { color:#f8f2e5 !important; }
h1,h2,h3 { font-family:'Playfair Display',serif; color:var(--navy); }
body,p,label,input,textarea,select { font-family:'DM Sans',sans-serif; }
.brand { border-bottom:1px solid rgba(216,155,50,.4); padding:1rem 0 1.3rem; margin-bottom:1.5rem; }
.brand-title { color:#f7d58b; font:700 1.45rem 'Playfair Display',serif; }
.brand-subtitle { color:#dce7ef; font-size:.82rem; margin-top:.25rem; }
.hero { background:linear-gradient(120deg,#102a43,#1f4b68); color:white; padding:2rem 2.2rem; border-radius:8px; margin-bottom:1.4rem; }
.hero h1 { color:#f7d58b; margin-bottom:.3rem; }
.hero p { color:#edf4f7; max-width:700px; }
.notice { background:#fff8e8; border-left:4px solid var(--gold); padding:.8rem 1rem; border-radius:4px; }
div[data-testid="stMetric"] { background:white; border-top:3px solid var(--gold); padding:1rem; border-radius:6px; }
.resource { background:white; padding:1rem 1.2rem; border-left:3px solid var(--gold); margin-bottom:.8rem; border-radius:4px; }
.resource a { color:var(--navy); font-weight:700; }
.member-badge { background:white; border:1px solid #d9e1e8; border-radius:8px; padding:1rem; text-align:center; min-height:110px; }
.member-badge strong { display:block; color:var(--navy); font:700 1.1rem 'Playfair Display',serif; }
.member-badge span { display:block; color:#66788a; font-size:.75rem; margin-top:.35rem; }
.sda-mark { color:#1477a8; border:2px solid #1477a8; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; width:42px; height:42px; font-weight:700; margin-bottom:.45rem; }
.pcm-mark { color:#b17616; border:2px solid #b17616; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; width:42px; height:42px; font-weight:700; margin-bottom:.45rem; }
.section-label { color:#f7d58b; font-size:.7rem; text-transform:uppercase; letter-spacing:.08em; margin:1rem 0 .35rem; }
.member-footer { border-top:1px solid #d9e1e8; margin-top:2rem; padding-top:1rem; color:#66788a; font-size:.82rem; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_students():
	columns = ["Jina kamili", "Namba ya usajili", "Programu", "Mwaka wa masomo", "Jinsia", "Simu", "Email", "Makazi", "Tarehe ya usajili", "Mkoa uliozaliwa", "wilayauliozaliwa"
, "Kata uliozaliwa", "Mtaa uliozaliwa", "Mkoa wa makazi", "Wilaya ya makazi", "Kata ya makazi", "Mtaa wa makazi"]
	if not DATA_FILE.exists():
		return pd.DataFrame(columns=columns)
	return pd.read_csv(DATA_FILE)


def save_students(data):
	data.to_csv(DATA_FILE, index=False)
	load_students.clear()


def add_student(student):
	students = load_students()
	if not students.empty and student["Namba ya usajili"] in students["Namba ya usajili"].astype(str).values:
		return False
	save_students(pd.concat([students, pd.DataFrame([student])], ignore_index=True))
	return True


@st.cache_data
def load_events():
	columns = ["Kichwa cha tukio", "Tarehe", "Muda", "Eneo", "Maelezo", "Picha URL"]
	if not EVENTS_FILE.exists():
		return pd.DataFrame(columns=columns)
	return pd.read_csv(EVENTS_FILE)


def save_events(data):
	data.to_csv(EVENTS_FILE, index=False)
	load_events.clear()


def show_remote_image(image_value, label="Picha"):
	image_url = str(image_value).strip()
	if not image_url or image_url.lower() == "nan":
		return
	if image_url.startswith(("https://", "http://")):
		try:
			st.image(image_url, caption=label, use_container_width=True)
		except Exception:
			st.warning(f"{label} haikuweza kufunguka. Hakikisha URL ya picha ni sahihi.")
	else:
		st.warning(f"{label} ina URL isiyo sahihi: `{image_url}`. Tumia `https://...`.")


@st.cache_data
def load_choir_events():
	columns = ["Kichwa", "Tarehe", "Muda", "Eneo", "Tangazo", "Picha URL"]
	if not CHOIR_EVENTS_FILE.exists():
		return pd.DataFrame(columns=columns)
	return pd.read_csv(CHOIR_EVENTS_FILE)


def save_choir_events(data):
	data.to_csv(CHOIR_EVENTS_FILE, index=False)
	load_choir_events.clear()


@st.cache_data
def load_choir_songs():
	columns = ["Jina la wimbo", "Aina", "Lugha", "Maelezo", "Link ya wimbo"]
	if not CHOIR_SONGS_FILE.exists():
		return pd.DataFrame(columns=columns)
	return pd.read_csv(CHOIR_SONGS_FILE)


def save_choir_songs(data):
	data.to_csv(CHOIR_SONGS_FILE, index=False)
	load_choir_songs.clear()


@st.cache_data
def load_leaders():
	columns = ["Nafasi", "Jina", "Majukumu", "Mawasiliano", "Picha"]
	if not LEADERS_FILE.exists():
		return pd.DataFrame(columns=columns)
	leaders = pd.read_csv(LEADERS_FILE)
	if "Picha" not in leaders.columns:
		leaders["Picha"] = ""
	return leaders[columns]


def save_leaders(data):
	data.to_csv(LEADERS_FILE, index=False)
	load_leaders.clear()


@st.cache_data
def load_branding():
	if not BRANDING_FILE.exists():
		return {"SDA Logo": "", "PCM Logo": ""}
	branding = pd.read_csv(BRANDING_FILE)
	return dict(zip(branding["Aina"], branding["Picha"]))


def save_branding(branding):
	data = pd.DataFrame([{"Aina": key, "Picha": value} for key, value in branding.items()])
	data.to_csv(BRANDING_FILE, index=False)
	load_branding.clear()


@st.cache_data
def load_questions():
	columns = ["Jina", "Email", "Swali", "Jibu", "Hali", "Tarehe"]
	if not QUESTIONS_FILE.exists():
		return pd.DataFrame(columns=columns)
	return pd.read_csv(QUESTIONS_FILE)


def save_questions(data):
	data.to_csv(QUESTIONS_FILE, index=False)
	load_questions.clear()


def admin_login_page():
	st.subheader("Kuingia kwa Admin")
	st.caption("Eneo hili ni kwa viongozi walioidhinishwa wa TUCASA UDSM Mabibo.")
	with st.form("admin_login_form"):
		admin_type = st.selectbox("Aina ya Admin", ["Admin Mkuu", "Admin Mdogo - Choir"])
		username = st.text_input("Username")
		password = st.text_input("Password", type="password")
		login = st.form_submit_button("Login", type="primary", use_container_width=True)
	if login:
		if admin_type == "Admin Mkuu" and username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
			st.session_state["admin_authenticated"] = True
			st.session_state["admin_role"] = "main_admin"
			st.success("Umeingia kama admin.")
			st.rerun()
		elif admin_type == "Admin Mdogo - Choir" and username == CHOIR_ADMIN_USERNAME and password == CHOIR_ADMIN_PASSWORD:
			st.session_state["admin_authenticated"] = True
			st.session_state["admin_role"] = "choir_admin"
			st.success("Umeingia kama Admin wa Choir.")
			st.rerun()
		else:
			st.error("Username au password si sahihi.")


def events_page():
	st.subheader("Matukio ya TUCASA")
	events = load_events()
	if events.empty:
		st.info("Bado hakuna matukio yaliyowekwa. Admin anaweza kuyaongeza kwenye Admin Panel.")
		return
	for _, event in events.iloc[::-1].iterrows():
		left, right = st.columns([1, 2])
		with left:
			show_remote_image(event["Picha URL"], "Picha ya tukio")
		with right:
			st.markdown(f"### {event['Kichwa cha tukio']}")
			st.write(f"**{event['Tarehe']} | {event['Muda']}**")
			st.write(f"**Eneo:** {event['Eneo']}")
			st.write(event["Maelezo"])
		st.markdown("---")


def admin_overview(students, events):
	st.subheader("Muhtasari wa mfumo")
	first, second, third, fourth = st.columns(4)
	first.metric("Wanafunzi", len(students))
	second.metric("Matukio", len(events))
	third.metric("Mabibo Hostel", int((students["Makazi"] == "Mabibo Hostel").sum()) if not students.empty else 0)
	fourth.metric("Programu", students["Programu"].nunique() if not students.empty else 0)
	st.info("Tumia menyu ya kushoto kusimamia taarifa za wanafunzi, matukio, picha na rasilimali za TUCASA.")


def admin_students_page(students):
	st.subheader("Usajili wa wanafunzi")
	if students.empty:
		st.info("Bado hakuna mwanafunzi aliyesajiliwa.")
		return
	search = st.text_input("Tafuta kwa jina au namba ya usajili")
	filtered = students
	if search.strip():
		mask = students["Jina kamili"].astype(str).str.contains(search, case=False, na=False) | students["Namba ya usajili"].astype(str).str.contains(search, case=False, na=False)
		filtered = students[mask]
	st.dataframe(filtered, use_container_width=True, hide_index=True)
	st.download_button("Pakua usajili (CSV)", students.to_csv(index=False), "tucasa_students.csv", "text/csv")


def admin_library_page():
	st.subheader("Usimamizi wa maktaba")
	st.write("Hivi ni vyanzo vinavyopatikana kwa watumiaji kwenye Maktaba ya Kisabato:")
	st.write("- Biblia ya King James Version (KJV)")
	st.write("- Vitabu na mafundisho ya Ellen G. White")
	st.write("- Masomo ya Biblia na Shule ya Sabato")
	st.write("- Afya ya akili kwa mtazamo wa Kisabato")
	st.write("- Vitabu vikubwa na vidogo vya nyimbo za Kristo")
	st.caption("Ushauri: ongeza links za PDF au tovuti zenye ruhusa ya kuzisambaza, badala ya kupakia vitabu vyenye hakimiliki bila idhini.")


def admin_questions_page():
	st.subheader("Maswali ya wanachama")
	questions = load_questions()
	if questions.empty:
		st.info("Bado hakuna swali lililotumwa na mwanachama.")
		return
	for index, item in questions.iloc[::-1].iterrows():
		st.markdown(f"**{item['Jina']}** | {item['Tarehe']} | Hali: `{item['Hali']}`")
		st.write(item["Swali"])
		if item["Hali"] == "Answered":
			st.success(f"Jibu: {item['Jibu']}")
		else:
			with st.form(f"answer_form_{index}"):
				answer = st.text_area("Andika jibu", key=f"answer_{index}")
				answer_button = st.form_submit_button("Hifadhi jibu")
			if answer_button:
				questions.loc[index, "Jibu"] = answer.strip()
				questions.loc[index, "Hali"] = "Answered"
				save_questions(questions)
				st.success("Jibu limehifadhiwa.")
				st.rerun()
		st.markdown("---")
	st.download_button("Pakua maswali (CSV)", questions.to_csv(index=False), "tucasa_questions.csv", "text/csv")


def admin_choir_page():
	st.subheader("Usimamizi wa Choir")
	st.caption("Ongeza matangazo, ratiba, ibada, mazoezi na picha za Choir.")
	with st.form("choir_event_form", clear_on_submit=True):
		st.write("**Ongeza tangazo au tukio la Choir**")
		first, second = st.columns(2)
		title = first.text_input("Kichwa cha tangazo *", placeholder="Mf. Mazoezi ya Choir")
		date = second.date_input("Tarehe")
		time = first.text_input("Muda", placeholder="Mf. saa 11:00 jioni")
		location = second.text_input("Eneo", placeholder="Mf. Mabibo Hostel")
		announcement = st.text_area("Tangazo / maelezo *")
		image_url = st.text_input("Picha URL", placeholder="https://example.com/choir.jpg")
		save_button = st.form_submit_button("Hifadhi tangazo", type="primary", use_container_width=True)
	if save_button:
		if not title.strip() or not announcement.strip():
			st.error("Weka kichwa na maelezo ya tangazo.")
		else:
			events = load_choir_events()
			record = {"Kichwa": title.strip(), "Tarehe": str(date), "Muda": time.strip(), "Eneo": location.strip(), "Tangazo": announcement.strip(), "Picha URL": image_url.strip()}
			save_choir_events(pd.concat([events, pd.DataFrame([record])], ignore_index=True))
			st.success("Tangazo la Choir limehifadhiwa.")

	st.write("**Matangazo yaliyopo**")
	events = load_choir_events()
	if not events.empty:
		st.dataframe(events, use_container_width=True, hide_index=True)
		st.download_button("Pakua matangazo ya Choir (CSV)", events.to_csv(index=False), "tucasa_choir_events.csv", "text/csv")

	st.markdown("---")
	st.subheader("Maktaba ya Nyimbo za Kwaya")
	st.caption("Ongeza nyimbo kwa kutumia links rasmi za audio, video au PDF yenye ruhusa.")
	with st.form("choir_song_form", clear_on_submit=True):
		first, second = st.columns(2)
		song_name = first.text_input("Jina la wimbo *")
		song_type = second.selectbox("Aina ya wimbo", ["Sifa", "Ibada", "Kwaya", "Vijana", "Maombi", "Uinjilisti"])
		language = first.selectbox("Lugha", ["Kiswahili", "English", "Nyingine"])
		song_description = second.text_input("Maelezo mafupi")
		song_url = st.text_input("Link ya wimbo (optional)", placeholder="https://youtube.com/... au https://example.com/song.pdf")
		uploaded_pdf = st.file_uploader("Au pakia PDF ya wimbo", type=["pdf"])
		add_song = st.form_submit_button("Hifadhi wimbo", type="primary", use_container_width=True)
	if add_song:
		if not song_name.strip() or (not song_url.strip() and uploaded_pdf is None):
			st.error("Weka jina na link ya wimbo au pakia PDF.")
		else:
			stored_pdf = ""
			if uploaded_pdf is not None:
				CHOIR_SONGS_DIR.mkdir(exist_ok=True)
				pdf_name = Path(uploaded_pdf.name).name
				pdf_path = CHOIR_SONGS_DIR / pdf_name
				pdf_path.write_bytes(uploaded_pdf.getbuffer())
				stored_pdf = str(pdf_path)
			songs = load_choir_songs()
			record = {"Jina la wimbo": song_name.strip(), "Aina": song_type, "Lugha": language, "Maelezo": song_description.strip(), "Link ya wimbo": song_url.strip() or stored_pdf}
			save_choir_songs(pd.concat([songs, pd.DataFrame([record])], ignore_index=True))
			st.success("Wimbo umeongezwa kwenye maktaba ya Kwaya.")

	songs = load_choir_songs()
	if not songs.empty:
		st.dataframe(songs, use_container_width=True, hide_index=True)
		st.download_button("Pakua maktaba ya nyimbo (CSV)", songs.to_csv(index=False), "tucasa_choir_songs.csv", "text/csv")


def admin_leadership_page():
	st.subheader("Usimamizi wa Uongozi wa Tawi")
	st.caption("Admin Mkuu ndiye anayeruhusiwa kuongeza au kusahihisha majina ya viongozi.")
	with st.form("leadership_form", clear_on_submit=True):
		first, second = st.columns(2)
		role = first.selectbox("Nafasi", ["Mwenyekiti wa Tawi", "Makamu Mwenyekiti", "Katibu wa Tawi", "Mweka Hazina", "Kiongozi wa Choir", "Kiongozi wa Maombi na Ustawi", "Nafasi nyingine"])
		name = second.text_input("Jina la kiongozi *")
		responsibility = st.text_area("Majukumu")
		contact = st.text_input("Mawasiliano", placeholder="Simu au email")
		leader_photo = st.file_uploader("Picha ya kiongozi", type=["png", "jpg", "jpeg", "webp", "image/png", "image/jpeg", "image/webp"])
		add_leader = st.form_submit_button("Hifadhi kiongozi", type="primary", use_container_width=True)
	if add_leader:
		if not name.strip():
			st.error("Weka jina la kiongozi.")
		else:
			photo_path = ""
			if leader_photo is not None:
				LEADERS_PHOTOS_DIR.mkdir(exist_ok=True)
				photo_name = Path(leader_photo.name).name
				photo_file = LEADERS_PHOTOS_DIR / photo_name
				photo_file.write_bytes(leader_photo.getbuffer())
				photo_path = str(photo_file)
			leaders = load_leaders()
			record = {"Nafasi": role, "Jina": name.strip(), "Majukumu": responsibility.strip(), "Mawasiliano": contact.strip(), "Picha": photo_path}
			save_leaders(pd.concat([leaders, pd.DataFrame([record])], ignore_index=True))
			st.success("Taarifa ya kiongozi imehifadhiwa.")

	leaders = load_leaders()
	if not leaders.empty:
		st.dataframe(leaders, use_container_width=True, hide_index=True)
		st.download_button("Pakua orodha ya viongozi (CSV)", leaders.to_csv(index=False), "tucasa_leaders.csv", "text/csv")


def admin_branding_page():
	st.subheader("Branding na Logo")
	st.caption("Import logo rasmi za Seventh-day Adventist Church na PCM zitakazoonekana kwa wanachama. Tumia PNG, JPG, JPEG au WEBP.")
	branding = load_branding()
	with st.form("branding_form", clear_on_submit=True):
		sda_logo = st.file_uploader("Import Logo ya Seventh-day Adventist Church", type=["png", "jpg", "jpeg", "webp", "image/png", "image/jpeg", "image/webp"])
		pcm_logo = st.file_uploader("Import Logo ya PCM", type=["png", "jpg", "jpeg", "webp", "image/png", "image/jpeg", "image/webp"])
		save_logos = st.form_submit_button("Hifadhi logo", type="primary", use_container_width=True)
	if save_logos:
		if sda_logo is None and pcm_logo is None:
			st.warning("Chagua angalau logo moja kabla ya kubonyeza Hifadhi logo.")
		else:
			try:
				BRANDING_DIR.mkdir(parents=True, exist_ok=True)
				for logo_type, uploaded_logo, base_name in [
					("SDA Logo", sda_logo, "sda_logo"),
					("PCM Logo", pcm_logo, "pcm_logo"),
				]:
					if uploaded_logo is not None:
						extension = Path(uploaded_logo.name).suffix.lower()
						if not extension:
							extension = ".png"
						logo_path = BRANDING_DIR / f"{base_name}{extension}"
						logo_path.write_bytes(uploaded_logo.getbuffer())
						branding[logo_type] = str(logo_path)
						st.write(f"{logo_type}: {uploaded_logo.size / 1024:.1f} KB")
				save_branding(branding)
				st.success("Logo zimehifadhiwa. Ukurasa utajionyesha upya sasa.")
				st.rerun()
			except OSError as error:
				st.error(f"Logo haikuhifadhiwa: {error}")

	st.write("**Logo zilizopo**")
	first, second = st.columns(2)
	with first:
		st.write("SDA Logo")
		if Path(str(branding.get("SDA Logo", ""))).is_file():
			st.image(branding["SDA Logo"], width=150)
		else:
			st.info("Bado hakuna logo ya SDA.")
	with second:
		st.write("PCM Logo")
		if Path(str(branding.get("PCM Logo", ""))).is_file():
			st.image(branding["PCM Logo"], width=150)
		else:
			st.info("Bado hakuna logo ya PCM.")


def admin_page():
	if not st.session_state.get("admin_authenticated", False):
		admin_login_page()
		return
	admin_role = st.session_state.get("admin_role", "main_admin")
	st.subheader("Admin Panel")
	if admin_role == "choir_admin":
		st.success("Umeingia kama Admin wa Choir. Unaweza kusimamia Choir tu.")
	else:
		st.success("Umeingia kwenye eneo la usimamizi wa TUCASA.")
	if st.button("Logout", key="admin_logout"):
		st.session_state["admin_authenticated"] = False
		st.session_state.pop("admin_role", None)
		st.rerun()
	if admin_role == "choir_admin":
		admin_choir_page()
		return
	students = load_students()
	events = load_events()
	admin_menu = st.radio("Menyu ya Admin", ["Muhtasari", "Usajili wa wanafunzi", "Maswali ya wanachama", "Uongozi wa tawi", "Matukio na picha", "Choir na matangazo", "Maktaba", "Branding na Logo", "Mipangilio"], horizontal=True)
	if admin_menu == "Muhtasari":
		admin_overview(students, events)
		return
	if admin_menu == "Usajili wa wanafunzi":
		admin_students_page(students)
		return
	if admin_menu == "Maktaba":
		admin_library_page()
		return
	if admin_menu == "Maswali ya wanachama":
		admin_questions_page()
		return
	if admin_menu == "Choir na matangazo":
		admin_choir_page()
		return
	if admin_menu == "Uongozi wa tawi":
		admin_leadership_page()
		return
	if admin_menu == "Branding na Logo":
		admin_branding_page()
		return
	if admin_menu == "Mipangilio":
		st.subheader("Mipangilio ya admin")
		st.write(f"**Username ya sasa:** `{ADMIN_USERNAME}`")
		st.write(f"**Username ya Admin wa Choir:** `{CHOIR_ADMIN_USERNAME}`")
		st.caption("Admin Mkuu: TUCASA_ADMIN_USERNAME na TUCASA_ADMIN_PASSWORD. Admin wa Choir: TUCASA_CHOIR_ADMIN_USERNAME na TUCASA_CHOIR_ADMIN_PASSWORD.")
		st.warning("Usiweke password halisi ndani ya faili la programu wakati wa kupeleka mfumo online.")
		return

	with st.form("event_form", clear_on_submit=True):
		st.subheader("Usimamizi wa matukio na picha")
		st.write("**Ongeza tukio jipya**")
		first, second = st.columns(2)
		title = first.text_input("Kichwa cha tukio *")
		date = second.date_input("Tarehe")
		time = first.text_input("Muda", placeholder="Mf. 10:00 - 13:00")
		location = second.text_input("Eneo", placeholder="Mf. Mabibo Hostel")
		description = st.text_area("Maelezo ya tukio")
		image_url = st.text_input("Picha URL", placeholder="https://example.com/picha.jpg")
		add_event = st.form_submit_button("Hifadhi tukio", type="primary", use_container_width=True)
	if add_event:
		if not title.strip():
			st.error("Weka kichwa cha tukio.")
		else:
			events = load_events()
			record = {"Kichwa cha tukio": title.strip(), "Tarehe": str(date), "Muda": time.strip(), "Eneo": location.strip(), "Maelezo": description.strip(), "Picha URL": image_url.strip()}
			save_events(pd.concat([events, pd.DataFrame([record])], ignore_index=True))
			st.success("Tukio limehifadhiwa.")

	st.write("**Matukio yaliyopo**")
	events = load_events()
	if not events.empty:
		st.dataframe(events, use_container_width=True, hide_index=True)
		st.download_button("Pakua matukio (CSV)", events.to_csv(index=False), "tucasa_events.csv", "text/csv")


def student_form():
	st.subheader("Usajili wa mwanafunzi mpya")
	st.caption("Jaza taarifa kwa usahihi. Taarifa zitatumika kwa uratibu wa TUCASA UDSM Mabibo.")
	with st.form("registration_form", clear_on_submit=True):
		first, second = st.columns(2)
		name = first.text_input("Jina kamili *")
		registration_number = second.text_input("Namba ya usajili *", placeholder="Mf. 2026-01-0001")
		program = first.selectbox("Programu ya masomo", ["Chagua...", "BSc", "BA", "BEd", "LLB", "MD", "Engineering", "Nyingine"])
		year = second.selectbox("Mwaka wa masomo", ["Mwaka wa kwanza", "Mwaka wa pili", "Mwaka wa tatu", "Mwaka wa nne", "Postgraduate"])
		gender = first.selectbox("Jinsia", ["Haijatajwa", "Mwanaume", "Mwanamke"])
		phone = second.text_input("Namba ya simu *", placeholder="07XXXXXXXX")
		email = first.text_input("Barua pepe")
		residence = second.selectbox("Eneo la makazi", ["Mabibo Hostel", "Hostel nyingine", "Nje ya chuo"])
		consent = st.checkbox("Ninakubali TUCASA kutumia taarifa hizi kwa mawasiliano ya uanachama. *")
		submitted = st.form_submit_button("Tuma usajili", type="primary", use_container_width=True)
	if submitted:
		if not name.strip() or not registration_number.strip() or not phone.strip() or not consent:
			st.error("Jaza sehemu zote zenye * na ukubali matumizi ya taarifa.")
		elif program == "Chagua...":
			st.error("Chagua programu ya masomo.")
		elif add_student({"Jina kamili":name.strip(), "Namba ya usajili":registration_number.strip(), "Programu":program, "Mwaka wa masomo":year, "Jinsia":gender, "Simu":phone.strip(), "Email":email.strip(), "Makazi":residence, "Tarehe ya usajili":pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")}):
			st.success("Usajili umepokelewa. Karibu TUCASA UDSM Mabibo!")
		else:
			st.warning("Namba hii ya usajili ipo tayari kwenye mfumo.")


def faq_page():
	st.subheader("Maswali na Majibu")
	st.caption("Majibu ya maswali yanayoulizwa mara kwa mara na wanachama wa TUCASA UDSM Mabibo.")
	with st.form("member_question_form", clear_on_submit=True):
		st.write("**Uliza swali kwa viongozi wa TUCASA**")
		question_name = st.text_input("Jina lako *")
		question_email = st.text_input("Email au namba ya simu")
		question_text = st.text_area("Swali lako *")
		send_question = st.form_submit_button("Tuma swali", type="primary")
	if send_question:
		if not question_name.strip() or not question_text.strip():
			st.error("Jaza jina na swali lako.")
		else:
			questions_data = load_questions()
			record = {"Jina": question_name.strip(), "Email": question_email.strip(), "Swali": question_text.strip(), "Jibu": "", "Hali": "Pending", "Tarehe": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")}
			save_questions(pd.concat([questions_data, pd.DataFrame([record])], ignore_index=True))
			st.success("Swali limetumwa kwa admin. Utapata jibu likishajibiwa.")

	questions_data = load_questions()
	answered_questions = questions_data[questions_data["Hali"] == "Answered"] if not questions_data.empty else questions_data
	if not answered_questions.empty:
		st.write("**Majibu kutoka kwa viongozi**")
		for _, item in answered_questions.iloc[::-1].iterrows():
			with st.expander(item["Swali"]):
				st.write(item["Jibu"])
	questions = [
		("TUCASA ni nini?", "TUCASA ni jumuiya ya wanafunzi Waadventista inayosaidia kujenga imani, urafiki, masomo na huduma chuoni."),
		("Ninawezaje kujisajili?", "Fungua menyu ya Usajili, jaza taarifa zenye alama ya *, kubali matumizi ya taarifa, kisha bonyeza Tuma usajili."),
		("Kwa nini namba ya usajili inahitajika?", "Inasaidia kutambua mwanafunzi mmoja tu na kuzuia usajili kujirudia."),
		("Ninawezaje kujiunga na WhatsApp group?", "Bonyeza kitufe cha Jiunge na WhatsApp group kilicho kwenye sidebar ya mfumo."),
		("Matukio ya TUCASA yanaonekana wapi?", "Fungua menyu ya Matukio na Picha. Hapo utaona tarehe, muda, eneo, maelezo na picha za matukio."),
		("Ninaweza kupata Biblia ya King James wapi?", "Fungua Maktaba ya Kisabato, kisha chagua tab ya Biblia ya King James. Utapata links za BibleGateway, YouVersion na Bible Hub."),
		("Vitabu vya Ellen G. White vinapatikana wapi?", "Fungua Maktaba ya Kisabato, chagua Ellen G. White, kisha chagua kitabu au Maktaba kuu ya EGW Writings."),
		("Nifanye nini nikihitaji msaada wa afya ya akili?", "Ongea na mtu unayemwamini, mshauri wa chuo, kiongozi wa kiroho au mtaalamu wa afya. Ukiwa katika hatari ya haraka, tafuta huduma ya dharura ya eneo lako."),
		("Ninawezaje kutoa wazo au kuuliza swali jipya?", "Wasiliana na viongozi wa TUCASA kupitia WhatsApp group au tumia mawasiliano rasmi ya tawi."),
	]
	search = st.text_input("Tafuta swali", placeholder="Mf. usajili, WhatsApp, Biblia...")
	for question, answer in questions:
		if not search.strip() or search.lower() in f"{question} {answer}".lower():
			with st.expander(question):
				st.write(answer)


def choir_page():
	st.subheader("Choir ya TUCASA UDSM Mabibo")
	st.caption("Huduma ya muziki kwa sifa, ibada, uinjilisti na kujenga umoja wa wanachama.")
	st.markdown('<div class="hero"><h1>Karibu kwenye Choir</h1><p>Tumwimbie Bwana kwa moyo, nidhamu na upendo. Kila mwanachama mwenye kipawa au nia ya kujifunza anakaribishwa.</p></div>', unsafe_allow_html=True)
	choir_events = load_choir_events()
	if not choir_events.empty:
		st.write("**Matangazo na matukio ya Choir**")
		for _, event in choir_events.iloc[::-1].iterrows():
			left, right = st.columns([1, 2])
			with left:
				show_remote_image(event["Picha URL"], "Picha ya Choir")
			with right:
				st.markdown(f"### {event['Kichwa']}")
				st.write(f"**{event['Tarehe']} | {event['Muda']}**")
				st.write(f"**Eneo:** {event['Eneo']}")
				st.write(event["Tangazo"])
			st.markdown("---")
	first, second, third = st.columns(3)
	first.metric("Huduma", "Sifa na ibada")
	second.metric("Mazoezi", "Kila wiki")
	third.metric("Wanachama", "Wote wanakaribishwa")

	st.write("**Ratiba inayopendekezwa**")
	schedule = pd.DataFrame([
		{"Siku": "Jumatano", "Muda": " saa 11:00 jioni", "Shughuli": "Mazoezi ya sauti na nyimbo"},
		{"Siku": "Ijumaa", "Muda": "saa 10:00 jioni", "Shughuli": "Maandalizi ya ibada"},
		{"Siku": "Sabato", "Muda": "Baada ya ibada", "Shughuli": "Tathmini na mipango ya wiki"},
	])
	st.dataframe(schedule, use_container_width=True, hide_index=True)

	with st.expander("Majukumu ya mwanachama wa choir"):
		st.write("- Kufika kwa wakati kwenye mazoezi na ibada.")
		st.write("- Kujifunza nyimbo na kutunza sauti.")
		st.write("- Kushirikiana kwa heshima na waimbaji wengine.")
		st.write("- Kuishi maisha yanayoendana na huduma ya Kikristo.")
	with st.expander("Nataka kujiunga na choir"):
		st.write("Wasiliana na viongozi wa TUCASA kupitia WhatsApp group ili upate taarifa ya majaribio na ratiba rasmi.")
		st.link_button("Wasiliana kupitia WhatsApp", WHATSAPP_GROUP_URL)

	st.write("**Maktaba ya Nyimbo za Kwaya**")
	st.caption("Nyimbo zilizowekwa na admin kwa ajili ya mazoezi na huduma.")
	songs = load_choir_songs()
	if songs.empty:
		st.info("Maktaba ya nyimbo bado haijawekewa nyimbo. Admin anaweza kuziongeza kupitia Admin Panel.")
	else:
		search_song = st.text_input("Tafuta wimbo", placeholder="Mf. sifa, Kiswahili, jina la wimbo...")
		filtered_songs = songs
		if search_song.strip():
			search_text = songs.astype(str).agg(" ".join, axis=1)
			filtered_songs = songs[search_text.str.contains(search_song, case=False, na=False)]
		for song_index, song in filtered_songs.iterrows():
			st.markdown(f'<div class="resource"><strong>{song["Jina la wimbo"]}</strong> | {song["Aina"]} | {song["Lugha"]}<br>{song["Maelezo"]}</div>', unsafe_allow_html=True)
			resource_path = Path(str(song["Link ya wimbo"]))
			if resource_path.is_file() and resource_path.suffix.lower() == ".pdf":
				st.download_button("Pakua PDF ya wimbo", resource_path.read_bytes(), resource_path.name, "application/pdf", key=f"song_pdf_{song_index}")
			elif str(song["Link ya wimbo"]).strip():
				st.link_button("Fungua wimbo", str(song["Link ya wimbo"]))

	st.write("**Rasilimali za ziada za nyimbo**")
	st.markdown('<div class="resource"><a href="https://hymnary.org/" target="_blank">Hymnary.org</a><br>Tafuta nyimbo, hymnals na maneno ya nyimbo za Kikristo.</div>', unsafe_allow_html=True)
	st.markdown('<div class="resource"><a href="https://adventist.org/music/" target="_blank">Adventist Music</a><br>Rasilimali za muziki na ibada za Waadventista.</div>', unsafe_allow_html=True)


def leadership_page():
	st.subheader("Uongozi wa Tawi la TUCASA UDSM Mabibo Hostel")
	st.caption("Muundo wa uongozi unaoratibu huduma, ustawi na shughuli za wanafunzi Wasabato Mabibo Hostel.")
	st.markdown('<div class="hero"><h1>Uongozi wa Tawi</h1><p>Viongozi wetu wanahudumu kwa uwajibikaji, ushirikiano na moyo wa Kikristo.</p></div>', unsafe_allow_html=True)

	leaders = load_leaders()
	if leaders.empty:
		st.info("Majina ya viongozi yataonekana hapa baada ya Admin Mkuu kuyaongeza kwenye Admin Panel.")
	else:
		for _, leader in leaders.iterrows():
			photo_path = Path(str(leader["Picha"]))
			if photo_path.is_file():
				st.image(str(photo_path), width=160)
			contact = f"<br>Mawasiliano: {leader['Mawasiliano']}" if str(leader["Mawasiliano"]).strip() else ""
			st.markdown(f'<div class="resource"><strong>{leader["Nafasi"]}</strong><br><span>{leader["Jina"]}</span><br>{leader["Majukumu"]}{contact}</div>', unsafe_allow_html=True)

	st.subheader("Wasiliana na Uongozi")
	st.write("Kwa usajili, matukio, maswali au msaada wa mwanachama, wasiliana na viongozi kupitia group rasmi la WhatsApp.")
	st.link_button("Wasiliana na TUCASA WhatsApp", WHATSAPP_GROUP_URL)
	st.info("Majina na mawasiliano ya viongozi yataongezwa na Admin Mkuu baada ya kupokea taarifa rasmi za tawi.")


def member_home_page(students, events):
	branding = load_branding()
	st.markdown('<div class="hero"><h1>TUCASA UDSM Mabibo Hostel</h1><p>Jumuiya ya wanafunzi Wasabato kwa imani, urafiki, huduma na mafanikio ya masomo.</p></div>', unsafe_allow_html=True)
	brand_one, brand_two = st.columns(2)
	with brand_one:
		if Path(str(branding.get("SDA Logo", ""))).is_file():
			st.image(branding["SDA Logo"], width=90)
		st.markdown('<div class="member-badge"><span class="sda-mark">SDA</span><strong>Seventh-day Adventist Church</strong><span>Imani, huduma na tumaini</span></div>', unsafe_allow_html=True)
	with brand_two:
		if Path(str(branding.get("PCM Logo", ""))).is_file():
			st.image(branding["PCM Logo"], width=90)
		st.markdown('<div class="member-badge"><span class="pcm-mark">PCM</span><strong>Public Campus Ministries</strong><span>Huduma ya wanafunzi vyuoni</span></div>', unsafe_allow_html=True)
	st.write("")
	first, second, third = st.columns(3)
	first.metric("Wanachama waliosajiliwa", len(students))
	second.metric("Matukio yajayo", len(events))
	third.metric("Jumuiya", "TUCASA Mabibo")
	st.subheader("Karibu kwenye jumuiya")
	st.write("Tumia menyu upande wa kushoto kufikia usajili, maswali na majibu, uongozi, Choir, matukio na Maktaba ya Kisabato.")
	if not events.empty:
		st.subheader("Tukio la hivi karibuni")
		latest = events.iloc[-1]
		st.markdown(f'<div class="resource"><strong>{latest["Kichwa cha tukio"]}</strong><br>{latest["Tarehe"]} | {latest["Muda"]} | {latest["Eneo"]}<br>{latest["Maelezo"]}</div>', unsafe_allow_html=True)
	st.markdown('<div class="member-footer">TUCASA UDSM Mabibo Hostel | Seventh-day Adventist Church | Public Campus Ministries</div>', unsafe_allow_html=True)


def analytics_page(students):
	st.subheader("Uchambuzi wa usajili")
	if students.empty:
		st.info("Bado hakuna usajili. Tumia ukurasa wa Usajili kuanza.")
		return
	cards = st.columns(4)
	cards[0].metric("Jumla ya wanafunzi", len(students))
	cards[1].metric("Waliosajiliwa leo", int(students["Tarehe ya usajili"].str.startswith(pd.Timestamp.now().strftime("%Y-%m-%d")).sum()))
	cards[2].metric("Mabibo Hostel", int((students["Makazi"] == "Mabibo Hostel").sum()))
	cards[3].metric("Programu tofauti", students["Programu"].nunique())
	left, right = st.columns(2)
	with left:
		st.write("**Usajili kwa programu**")
		st.bar_chart(students["Programu"].value_counts())
	with right:
		st.write("**Usajili kwa mwaka wa masomo**")
		st.bar_chart(students["Mwaka wa masomo"].value_counts())
	st.write("**Orodha ya usajili**")
	st.dataframe(students, use_container_width=True, hide_index=True)
	st.download_button("Pakua taarifa za usajili (CSV)", students.to_csv(index=False), "tucasa_students.csv", "text/csv")


def library_page():
	st.subheader("Maktaba ya Kisabato")
	st.caption("Biblia, masomo ya shule ya Sabato, na vitabu vya Ellen G. White kwa ajili ya jumuiya ya TUCASA.")
	bible_tab, egw_tab, lessons_tab, mental_health_tab, songs_tab = st.tabs(["Biblia ya King James", "Ellen G. White", "Masomo ya Kisabato", "Afya ya Akili", "Nyimbo za Kristo"])

	with bible_tab:
		st.write("**King James Version (KJV)**")
		st.caption("Soma Biblia ya Kiingereza ya King James mtandaoni. Tumia search ya tovuti kuchagua kitabu na sura.")
		bible_resources = [
			("Biblia nzima - BibleGateway KJV", "Vitabu vyote vya Agano la Kale na Jipya.", "https://www.biblegateway.com/versions/king-james-version-kjv-bible/"),
			("KJV Bible - YouVersion", "Soma na kuweka alama kwenye mistari unayoipenda.", "https://www.bible.com/versions/1-kjv-king-james-version"),
			("Bible Hub KJV", "Tafuta kitabu, sura, mstari na mafafanuzi.", "https://biblehub.com/kjv/"),
		]
		for title, description, url in bible_resources:
			st.markdown(f'<div class="resource"><a href="{url}" target="_blank">{title}</a><br>{description}</div>', unsafe_allow_html=True)

	with egw_tab:
		st.write("**Mafundisho na vitabu vya Ellen G. White**")
		st.caption("Mkusanyiko wa maandiko kwa kusoma, kutafuta mada, na kujifunza kwa kina.")
		egw_resources = [
			("EGW Writings - Maktaba kuu", "Tafuta maandiko, vitabu na mada mbalimbali.", "https://egwwritings.org/"),
			("Steps to Christ", "Mafundisho ya kumjua Kristo na kukua katika imani.", "https://egwwritings.org/read/128.1"),
			("The Great Controversy", "Historia ya pambano kuu na tumaini la Biblia.", "https://egwwritings.org/read/132.1"),
			("Education", "Misingi ya elimu ya Kikristo na maendeleo ya tabia.", "https://egwwritings.org/read/29.1"),
			("Messages to Young People", "Ushauri kwa vijana katika masomo, kazi na huduma.", "https://egwwritings.org/read/159.1"),
		]
		for title, description, url in egw_resources:
			st.markdown(f'<div class="resource"><a href="{url}" target="_blank">{title}</a><br>{description}</div>', unsafe_allow_html=True)

	with lessons_tab:
		st.write("**Masomo ya Biblia na Shule ya Sabato**")
		lesson_resources = [
			("Sabbath School Lessons", "Masomo ya robo mwaka kwa watu wazima na vijana.", "https://www.sabbath.school/"),
			("Adventist Lesson", "Masomo, audio na video za kujifunza kila wiki.", "https://adventistlesson.org/"),
			("Biblia kwa Kiswahili", "Soma Biblia ya Kiswahili kwa ajili ya kujifunza na kulinganisha.", "https://www.bible.com/sw"),
		]
		for title, description, url in lesson_resources:
			st.markdown(f'<div class="resource"><a href="{url}" target="_blank">{title}</a><br>{description}</div>', unsafe_allow_html=True)

	with mental_health_tab:
		st.write("**Afya ya Akili kwa Mtazamo wa Kikristo wa Kisabato**")
		st.caption("Rasilimali hizi ni za kujifunza na kutafakari. Hazibadilishi ushauri wa daktari, mshauri au mtaalamu wa afya ya akili.")
		st.info("Ukiwa katika hatari ya kujiumiza au kumdhuru mtu mwingine, tafuta msaada wa dharura mara moja kutoka huduma za eneo lako, hospitali, au mtu unayemwamini.")
		mental_resources = [
			("Mind, Character, and Personality - Ellen G. White", "Mafundisho kuhusu akili, tabia, hisia, mawazo na maendeleo ya utu.", "https://egwwritings.org/read/123.1"),
			("The Ministry of Healing - Ellen G. White", "Kanuni za maisha yenye afya, uwiano wa mwili, akili na roho.", "https://egwwritings.org/read/135.1"),
			("Counsels on Health - Ellen G. White", "Ushauri kuhusu afya, mapumziko, nidhamu na mtindo wa maisha.", "https://egwwritings.org/"),
			("Adventist Health", "Rasilimali za afya ya mwili, akili na maisha yenye uwiano kutoka kanisa la Waadventista.", "https://health.adventist.org/"),
			("Adventist Mental Health", "Makala na nyenzo za kujenga ustawi wa akili na huduma ya huruma.", "https://mentalhealth.adventist.org/"),
		]
		for title, description, url in mental_resources:
			st.markdown(f'<div class="resource"><a href="{url}" target="_blank">{title}</a><br>{description}</div>', unsafe_allow_html=True)

	with songs_tab:
		st.write("**Vitabu vya Nyimbo za Kristo**")
		st.caption("Nyimbo za sifa, ibada na uinjilisti kwa matumizi ya TUCASA UDSM Mabibo.")
		st.info("Kwa vitabu vyenye hakimiliki, tumia vyanzo rasmi au ruhusa ya wachapishaji. Unaweza kuongeza PDF zenu zenye ruhusa baadaye.")
		st.write("**Vitabu vikubwa vya nyimbo**")
		large_songbooks = [
			("Hymnary.org", "Maktaba kubwa ya nyimbo za Kikristo, vitabu vya nyimbo na search ya nyimbo.", "https://hymnary.org/"),
			("Seventh-day Adventist Hymnal", "Tafuta nyimbo za SDA kwa kichwa, namba au maneno ya wimbo.", "https://hymnary.org/hymnal/SDAH"),
			("Adventist Music", "Rasilimali rasmi za muziki, ibada na nyimbo za Waadventista.", "https://adventist.org/music/"),
		]
		for title, description, url in large_songbooks:
			st.markdown(f'<div class="resource"><a href="{url}" target="_blank">{title}</a><br>{description}</div>', unsafe_allow_html=True)

		st.write("**Vitabu vidogo vya nyimbo**")
		small_songbooks = [
			("Nyimbo za kwaya na vijana", "Tafuta nyimbo fupi za sifa, vijana, kwaya na vikundi vidogo.", "https://hymnary.org/search?qu=young+people+hymns"),
			("Nyimbo za ibada na maombi", "Mkusanyiko wa nyimbo za kutafakari na kuabudu.", "https://hymnary.org/search?qu=worship+and+prayer+hymns"),
			("Nyimbo za Kiswahili", "Tafuta nyimbo za Kikristo kwa lugha ya Kiswahili na lugha nyingine.", "https://www.youtube.com/results?search_query=nyimbo+za+Kikristo+za+Kiswahili"),
		]
		for title, description, url in small_songbooks:
			st.markdown(f'<div class="resource"><a href="{url}" target="_blank">{title}</a><br>{description}</div>', unsafe_allow_html=True)


def main():
	branding = load_branding()
	st.sidebar.markdown('<div class="brand"><div class="brand-title">TUCASA UDSM</div><div class="brand-subtitle">Mabibo Hostel | Tawi la Wanafunzi Wasabato</div><div class="section-label">Seventh-day Adventist Church | PCM</div></div>', unsafe_allow_html=True)
	if Path(str(branding.get("SDA Logo", ""))).is_file():
		st.sidebar.image(branding["SDA Logo"], width=90)
	if Path(str(branding.get("PCM Logo", ""))).is_file():
		st.sidebar.image(branding["PCM Logo"], width=90)
	st.sidebar.markdown('<div class="section-label">Mwanachama</div>', unsafe_allow_html=True)
	page = st.sidebar.radio("Menyu ya mwanachama", ["Karibu", "Usajili", "Maswali na Majibu", "Uongozi wa Tawi"], label_visibility="collapsed")
	st.sidebar.markdown('<div class="section-label">Huduma na jamii</div>', unsafe_allow_html=True)
	service_page = st.sidebar.radio("Huduma", ["Hakuna", "Choir", "Matukio na Picha"], label_visibility="collapsed")
	st.sidebar.markdown('<div class="section-label">Maktaba</div>', unsafe_allow_html=True)
	library_choice = st.sidebar.radio("Maktaba", ["Hakuna", "Maktaba ya Kisabato"], label_visibility="collapsed")
	st.sidebar.markdown('<div class="section-label">Taarifa</div>', unsafe_allow_html=True)
	info_choice = st.sidebar.radio("Taarifa", ["Hakuna", "Uchambuzi"], label_visibility="collapsed")
	st.sidebar.markdown("---")
	st.sidebar.link_button("Jiunge na WhatsApp group", WHATSAPP_GROUP_URL, use_container_width=True)
	st.sidebar.markdown('<div style="text-align:center; color:#f7d58b; font-size:.75rem; padding:.8rem 0;">SDA | PCM<br><span style="color:#dce7ef;">Faith • Service • Community</span></div>', unsafe_allow_html=True)
	st.sidebar.markdown('<div class="section-label">Usimamizi</div>', unsafe_allow_html=True)
	admin_choice = st.sidebar.radio("Admin", ["Hakuna", "Admin Login"], label_visibility="collapsed")
	students = load_students()
	events = load_events()
	if admin_choice == "Admin Login":
		admin_page()
		return
	if service_page != "Hakuna":
		page = service_page
	elif library_choice != "Hakuna":
		page = library_choice
	elif info_choice != "Hakuna":
		page = info_choice
	if page == "Karibu":
		member_home_page(students, events)
	elif page == "Usajili": student_form()
	elif page == "Maswali na Majibu": faq_page()
	elif page == "Uongozi wa Tawi": leadership_page()
	elif page == "Choir": choir_page()
	elif page == "Matukio na Picha": events_page()
	elif page == "Uchambuzi": analytics_page(students)
	elif page == "Maktaba ya Kisabato": library_page()


if __name__ == "__main__":
	main()



