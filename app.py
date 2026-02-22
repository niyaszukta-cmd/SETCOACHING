"""
Kerala SET English Literature & Linguistics — Practice App v3
Single-file · Streamlit Cloud compatible · Dark-mode safe
Author: NYZTrade Education Platform 2026
"""

import streamlit as st
import anthropic, json, random, re
from datetime import datetime

st.set_page_config(
    page_title="Kerala SET Practice | NYZTrade",
    page_icon="📚", layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
#  CSS  – all inline styles use explicit hex values, no CSS vars that dark-mode breaks
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
#MainMenu,footer,header{visibility:hidden}
.block-container{padding-top:.8rem;padding-bottom:2rem;max-width:980px}
*{font-family:'Inter',sans-serif}

/* header */
.app-hdr{background:linear-gradient(135deg,#1a3a6b 0%,#0d2347 100%);color:#fff;
  padding:1.2rem 1.8rem;border-radius:14px;margin-bottom:1.2rem;
  display:flex;align-items:center;justify-content:space-between;
  box-shadow:0 6px 28px rgba(26,58,107,.28)}
.app-hdr h1{font-family:'Playfair Display',serif;font-size:1.7rem;margin:0;color:#fff}
.app-hdr .sub{font-size:.8rem;opacity:.75;color:#fff;margin-top:2px}
.app-hdr .bdg{background:#d4a017;color:#1c1c2e;font-weight:700;font-size:.7rem;
  padding:3px 10px;border-radius:20px;text-transform:uppercase;letter-spacing:.5px}

/* ── Force light rendering on all white-background cards ── */
.sc,.qcard,.tcard,.dcard,.ksec,.acard,.tlev{color-scheme:light !important}

/* stat cards */
.srow{display:flex;gap:10px;margin-bottom:1.2rem;flex-wrap:wrap}
.sc{background:#ffffff !important;border-radius:10px;padding:.9rem 1.1rem;flex:1 1 120px;
  box-shadow:0 3px 16px rgba(0,0,0,.09);min-width:100px;color-scheme:light}
.sc .lbl{font-size:.68rem;color:#5a6a7d !important;text-transform:uppercase;letter-spacing:.5px;font-weight:600}
.sc .val{font-size:1.75rem;font-weight:700;line-height:1.1;margin-top:2px}
.sc-blue  {border-left:4px solid #1a3a6b} .sc-blue  .val{color:#1a3a6b !important}
.sc-green {border-left:4px solid #27ae60} .sc-green .val{color:#1e7e44 !important}
.sc-gold  {border-left:4px solid #d4a017} .sc-gold  .val{color:#8a6200 !important}
.sc-red   {border-left:4px solid #c0392b} .sc-red   .val{color:#962020 !important}

/* question card */
.qcard{background:#ffffff !important;border-radius:14px;padding:1.6rem 1.8rem;
  box-shadow:0 3px 16px rgba(0,0,0,.09);border:1px solid #dce3ee;margin-bottom:.8rem}
.qnum{font-size:.7rem;font-weight:700;color:#5a6a7d !important;text-transform:uppercase;
  letter-spacing:1px;margin-bottom:.4rem}
.qtags{display:flex;gap:5px;margin-bottom:.7rem;flex-wrap:wrap}
.tag{font-size:.66rem;font-weight:600;padding:2px 8px;border-radius:20px;text-transform:uppercase;letter-spacing:.4px}
.tag-def {background:#e8eef7;color:#1a3a6b !important}
.tag-ai  {background:#fff3e0;color:#c45000 !important}
.tag-hard{background:#fce4ec;color:#b71c1c !important}
.tag-easy{background:#e8f5e9;color:#1b5e20 !important}
.tag-med {background:#e3f2fd;color:#0d47a1 !important}
.qtext{font-size:1rem;font-weight:500;color:#1c1c2e !important;line-height:1.65;margin-bottom:1.2rem;white-space:pre-wrap}

/* progress */
.pw{background:#dce3ee;border-radius:20px;height:7px;margin-bottom:.8rem;overflow:hidden}
.pb{height:100%;border-radius:20px;background:linear-gradient(90deg,#1a3a6b,#2980b9);transition:width .4s}

/* result — dark bg, always white text */
.rcard{background:linear-gradient(135deg,#1a3a6b,#0d2347) !important;color:#fff !important;
  border-radius:18px;padding:2.2rem 1.8rem;text-align:center;margin:1rem 0;
  box-shadow:0 10px 36px rgba(26,58,107,.28)}
.rscore{font-size:3.6rem;font-weight:800;color:#fff !important;letter-spacing:-2px}
.rtotal{font-size:.95rem;opacity:.75;color:#fff !important;margin-top:-4px}
.rgrade{font-size:1.3rem;font-weight:600;color:#fff !important;margin-top:.8rem}

/* topic perf card */
.tcard{background:#ffffff !important;border-radius:10px;padding:12px 14px;margin-bottom:7px;
  box-shadow:0 2px 10px rgba(0,0,0,.07);display:flex;align-items:center;gap:12px}
.tcard-name{font-weight:700;font-size:.93rem;color:#1c1c2e !important}
.tcard-sub{font-size:.74rem;color:#5a6a7d !important;margin-top:2px}
.tcard-pct{font-size:1.55rem;font-weight:800;min-width:70px;text-align:right}
.tcard-lbl{font-size:.68rem;text-align:right;margin-top:1px}

/* diff card */
.dcard{background:#ffffff !important;border-radius:12px;padding:16px 13px;text-align:center;
  box-shadow:0 2px 10px rgba(0,0,0,.07)}
.dcard-pct{font-size:1.85rem;font-weight:800}
.dcard-name{font-weight:700;margin-top:3px;color:#1c1c2e !important;font-size:.9rem}
.dcard-sub{font-size:.74rem;color:#5a6a7d !important;margin-top:2px}

/* knowledge sections */
.ksec{background:#ffffff !important;border-radius:12px;padding:1.3rem 1.5rem;margin-bottom:.8rem;
  box-shadow:0 2px 10px rgba(0,0,0,.07);border-left:4px solid #1a3a6b}
.ksec h4{font-size:1rem;font-weight:700;color:#1a3a6b !important;margin:0 0 .5rem 0}
.ksec p,.ksec li{font-size:.88rem;color:#2c2c3e !important;line-height:1.6;margin:0}
.ksec ul{padding-left:1.2rem;margin:.4rem 0 0 0}

/* quote card — dark bg, always white text */
.qquote{background:linear-gradient(135deg,#1a3a6b 0%,#0d2347 100%) !important;border-radius:12px;
  padding:1.4rem 1.6rem;margin-bottom:.8rem}
.qquote blockquote{font-style:italic;font-size:1rem;line-height:1.65;margin:0 0 .7rem 0;color:#fff !important}
.qquote .attr{font-size:.78rem;opacity:.8;color:#fff !important}

/* timeline */
.tlrow{display:flex;gap:0;margin-bottom:.45rem;align-items:flex-start}
.tlyr{background:#1a3a6b !important;color:#fff !important;font-weight:700;font-size:.78rem;
  padding:4px 10px;border-radius:6px 0 0 6px;min-width:65px;text-align:center}
.tlev{background:#f0f4fb !important;color:#1c1c2e !important;font-size:.83rem;padding:5px 13px;
  border-radius:0 6px 6px 0;flex:1;box-shadow:0 1px 5px rgba(0,0,0,.06)}

/* author card */
.acard{background:#ffffff !important;border-radius:12px;padding:1.2rem 1.4rem;margin-bottom:.7rem;
  box-shadow:0 2px 10px rgba(0,0,0,.07);border-top:3px solid #1a3a6b}
.acard-name{font-size:1rem;font-weight:700;color:#1a3a6b !important}
.acard-dates{font-size:.75rem;color:#5a6a7d !important;margin:.2rem 0 .5rem 0}
.acard-body{font-size:.84rem;color:#2c2c3e !important;line-height:1.6}
.acard-works{font-size:.8rem;color:#1565c0 !important;margin-top:.4rem;font-weight:600}

/* wrong answer review box */
.wrong-box{background:#fff8f8 !important;border-left:3px solid #e74c3c;border-radius:6px;
  padding:10px 14px;margin-bottom:8px}
.wrong-box .wq{font-weight:600;margin-bottom:5px;color:#1c1c2e !important}
.wrong-box .wy{font-size:.83rem;color:#c0392b !important}
.wrong-box .wc{font-size:.83rem;color:#1e7e44 !important}

/* method/teaching card */
.mcard{background:#f8faff !important;border-radius:10px;padding:1rem 1.2rem;
  margin-bottom:.6rem;border-left:4px solid #2980b9}
.mcard h5{font-size:.93rem;font-weight:700;color:#1a3a6b !important;margin:0 0 .3rem 0}
.mcard p{font-size:.84rem;color:#2c2c3e !important;margin:0;line-height:1.55}
.mcard .ctx{font-size:.76rem;color:#1565c0 !important;margin-top:.3rem;font-weight:600}

/* flashcard */
.flash{background:#ffffff !important;border-radius:14px;padding:2rem;text-align:center;
  box-shadow:0 4px 20px rgba(0,0,0,.10);border:2px solid #e8eef7;min-height:160px;
  display:flex;flex-direction:column;align-items:center;justify-content:center}
.flash-q{font-size:1.1rem;font-weight:600;color:#1c1c2e !important;line-height:1.6}
.flash-a{font-size:.95rem;color:#1e7e44 !important;font-weight:700;margin-top:.8rem}
.flash-hint{font-size:.78rem;color:#5a6a7d !important;margin-top:.4rem}

/* glossary */
.gterm{background:#ffffff !important;border-radius:8px;padding:.8rem 1rem;margin-bottom:.4rem;
  box-shadow:0 1px 6px rgba(0,0,0,.06);display:flex;gap:10px;align-items:baseline}
.gterm-word{font-weight:700;color:#1a3a6b !important;font-size:.92rem;min-width:160px}
.gterm-def{font-size:.85rem;color:#2c2c3e !important;line-height:1.55}

/* ai box */
.ai-box{background:linear-gradient(135deg,#1a1a2e,#16213e);border-radius:14px;
  padding:1.4rem;color:#fff;margin-bottom:.9rem}
.ai-box h3{font-family:'Playfair Display',serif;font-size:1.2rem;margin-bottom:.3rem;color:#fff}
.ai-box p{opacity:.72;font-size:.84rem;margin:0;color:#fff}

/* sidebar */
[data-testid="stSidebar"]{background:linear-gradient(180deg,#1a3a6b,#0d2347) !important}
[data-testid="stSidebar"] *{color:#ffffff !important}
[data-testid="stSidebar"] .stButton>button{
  width:100%;background:rgba(255,255,255,.10) !important;color:#fff !important;
  border:1px solid rgba(255,255,255,.22) !important;border-radius:7px;margin-bottom:2px}
[data-testid="stSidebar"] .stButton>button:hover{background:rgba(255,255,255,.20) !important}
.stButton>button[kind="primary"]{
  background:linear-gradient(135deg,#1a3a6b,#2980b9) !important;color:#fff !important;
  border:none !important;border-radius:9px !important;font-weight:600 !important;
  box-shadow:0 4px 14px rgba(26,58,107,.25) !important}
hr{border:none;border-top:1px solid #dce3ee;margin:1rem 0}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  QUESTION BANK
# ══════════════════════════════════════════════════════════════════════════════
QUESTION_BANK = [
    {"id":1,"topic":"World Literature","subtopic":"African Literature","q":"The novel Things Fall Apart was written by:","opts":["A) Wole Soyinka","B) Chinua Achebe","C) Ngugi wa Thiong'o","D) Ben Okri"],"ans":"B","difficulty":"easy"},
    {"id":2,"topic":"British Literature","subtopic":"Old English","q":"The Old English epic Beowulf is composed in:","opts":["A) Rhyming couplets","B) Alliterative verse","C) Blank verse","D) Terza rima"],"ans":"B","difficulty":"medium"},
    {"id":3,"topic":"British Literature","subtopic":"Modernism","q":"Identify the true statements about Virginia Woolf:\nStatement 1: She was a member of the Bloomsbury Group.\nStatement 2: She founded the Hogarth Press.","opts":["A) 1 only","B) 2 only","C) Both 1 & 2","D) Neither 1 nor 2"],"ans":"C","difficulty":"easy"},
    {"id":4,"topic":"American Literature","subtopic":"Poetry","q":"\"Because I could not stop for Death\" was written by:","opts":["A) Christina Rossetti","B) Emily Brontë","C) Emily Dickinson","D) Sylvia Plath"],"ans":"C","difficulty":"easy"},
    {"id":5,"topic":"Literary Theory","subtopic":"Deconstruction","q":"\"There is nothing outside the text\" is associated with:","opts":["A) New Criticism","B) Deconstruction","C) Reader-Response Theory","D) Psychoanalytic Criticism"],"ans":"B","difficulty":"medium"},
    {"id":6,"topic":"British Literature","subtopic":"Renaissance","q":"'Amoretti', a sonnet sequence, was written by:","opts":["A) Philip Sidney","B) Edmund Spenser","C) Christopher Marlowe","D) Michael Drayton"],"ans":"B","difficulty":"medium"},
    {"id":7,"topic":"Literary Theory","subtopic":"Criticism","q":"The term 'objective correlative' was coined by:","opts":["A) I.A. Richards","B) William Empson","C) T.S. Eliot","D) F.R. Leavis"],"ans":"C","difficulty":"medium"},
    {"id":8,"topic":"Literary Theory","subtopic":"Feminism","q":"The Feminine Mystique (1963) was written by:","opts":["A) Simone de Beauvoir","B) Betty Friedan","C) Kate Millett","D) Germaine Greer"],"ans":"B","difficulty":"medium"},
    {"id":9,"topic":"Literary Theory","subtopic":"Postcolonialism","q":"Orientalism (1978) was written by:","opts":["A) Homi Bhabha","B) Gayatri Spivak","C) Edward Said","D) Frantz Fanon"],"ans":"C","difficulty":"easy"},
    {"id":10,"topic":"British Literature","subtopic":"20th Century","q":"George Orwell's last novel:","opts":["A) Homage to Catalonia","B) Keep the Aspidistra Flying","C) Nineteen Eighty-Four","D) Coming Up for Air"],"ans":"C","difficulty":"easy"},
    {"id":11,"topic":"British Literature","subtopic":"Renaissance","q":"Milton's Paradise Lost is an epic in _____ books.","opts":["A) 10","B) 12","C) 14","D) 24"],"ans":"B","difficulty":"medium"},
    {"id":12,"topic":"British Literature","subtopic":"Romanticism","q":"Coleridge's phrase 'willing suspension of disbelief' appears in:","opts":["A) Biographia Literaria","B) Aids to Reflection","C) The Statesman's Manual","D) Lectures on Shakespeare"],"ans":"A","difficulty":"medium"},
    {"id":13,"topic":"British Literature","subtopic":"Medieval","q":"Chaucer's work modelled on Boccaccio's Decameron:","opts":["A) Troilus and Criseyde","B) The Canterbury Tales","C) The Book of the Duchess","D) The Parliament of Fowls"],"ans":"B","difficulty":"easy"},
    {"id":14,"topic":"British Literature","subtopic":"Victorian","q":"The writer who used the pen name 'Currer Bell':","opts":["A) Anne Brontë","B) Emily Brontë","C) Charlotte Brontë","D) George Eliot"],"ans":"C","difficulty":"easy"},
    {"id":15,"topic":"Linguistics","subtopic":"Phonetics","q":"In bilabial sounds, the primary articulators are:","opts":["A) Tongue tip and upper teeth","B) Both lips","C) Tongue back and velum","D) Tongue tip and alveolar ridge"],"ans":"B","difficulty":"medium"},
    {"id":16,"topic":"Linguistics","subtopic":"Phonology","q":"The minimal sound unit that distinguishes meaning is called a:","opts":["A) Morpheme","B) Phoneme","C) Sememe","D) Lexeme"],"ans":"B","difficulty":"easy"},
    {"id":17,"topic":"Linguistics","subtopic":"Language Acquisition","q":"The innate language acquisition capacity hypothesis is associated with:","opts":["A) B.F. Skinner","B) Jean Piaget","C) Noam Chomsky","D) Lev Vygotsky"],"ans":"C","difficulty":"easy"},
    {"id":18,"topic":"Linguistics","subtopic":"Semantics","q":"According to Saussure, the signifier-signified relationship is:","opts":["A) Natural and motivated","B) Arbitrary and conventional","C) Fixed and universal","D) Iconic and indexical"],"ans":"B","difficulty":"medium"},
    {"id":19,"topic":"British Literature","subtopic":"Drama","q":"Tom Stoppard's play retelling Hamlet from two minor characters' perspective:","opts":["A) Arcadia","B) Travesties","C) Rosencrantz and Guildenstern Are Dead","D) The Real Thing"],"ans":"C","difficulty":"medium"},
    {"id":20,"topic":"British Literature","subtopic":"Renaissance","q":"Doctor Faustus was written by:","opts":["A) Ben Jonson","B) John Webster","C) Thomas Kyd","D) Christopher Marlowe"],"ans":"D","difficulty":"easy"},
    {"id":21,"topic":"Literary Theory","subtopic":"Criticism","q":"The Great Tradition (1948) evaluating the English novel was written by:","opts":["A) I.A. Richards","B) F.R. Leavis","C) William Empson","D) Raymond Williams"],"ans":"B","difficulty":"medium"},
    {"id":22,"topic":"Literary Theory","subtopic":"Structuralism","q":"The term 'intertextuality' was introduced by:","opts":["A) Roland Barthes","B) Jacques Derrida","C) Julia Kristeva","D) Mikhail Bakhtin"],"ans":"C","difficulty":"medium"},
    {"id":23,"topic":"Literary Theory","subtopic":"Poststructuralism","q":"'The Order of Things' is a well-known work by:","opts":["A) Jacques Derrida","B) Michel Foucault","C) Roland Barthes","D) Jean Baudrillard"],"ans":"B","difficulty":"medium"},
    {"id":24,"topic":"British Literature","subtopic":"Victorian","q":"The Stones of Venice was written by:","opts":["A) Matthew Arnold","B) John Ruskin","C) Thomas Carlyle","D) Walter Pater"],"ans":"B","difficulty":"medium"},
    {"id":25,"topic":"Literary Theory","subtopic":"Marxism","q":"'Ideological State Apparatus' is a concept by:","opts":["A) Antonio Gramsci","B) Louis Althusser","C) Raymond Williams","D) Terry Eagleton"],"ans":"B","difficulty":"medium"},
    {"id":26,"topic":"Literary Theory","subtopic":"Feminism","q":"The term 'gynocriticism' was coined by:","opts":["A) Julia Kristeva","B) Hélène Cixous","C) Elaine Showalter","D) Sandra Gilbert"],"ans":"C","difficulty":"medium"},
    {"id":27,"topic":"Literary Theory","subtopic":"Feminism","q":"The term 'écriture féminine' was coined by:","opts":["A) Julia Kristeva","B) Luce Irigaray","C) Hélène Cixous","D) Simone de Beauvoir"],"ans":"C","difficulty":"medium"},
    {"id":28,"topic":"British Literature","subtopic":"Romanticism","q":"Wordsworth and Coleridge collaborated on:","opts":["A) Poems in Two Volumes","B) Lyrical Ballads","C) Sibylline Leaves","D) The Prelude"],"ans":"B","difficulty":"easy"},
    {"id":29,"topic":"British Literature","subtopic":"Victorian","q":"'Sweetness and light' in cultural discourse was coined by:","opts":["A) Thomas Carlyle","B) John Ruskin","C) Walter Pater","D) Matthew Arnold"],"ans":"D","difficulty":"medium"},
    {"id":30,"topic":"British Literature","subtopic":"Romanticism","q":"The poem interrupted by the 'person from Porlock':","opts":["A) In Praise of Limestone","B) In Xanadu","C) Abou Ben Adam","D) Kubla Khan"],"ans":"D","difficulty":"easy"},
    {"id":31,"topic":"British Literature","subtopic":"Victorian","q":"\"It was the best of times, it was the worst of times\" opens:","opts":["A) Bleak House","B) David Copperfield","C) A Tale of Two Cities","D) Dombey and Son"],"ans":"C","difficulty":"easy"},
    {"id":32,"topic":"British Literature","subtopic":"20th Century","q":"'Dulce et Decorum Est' was written by:","opts":["A) Rupert Brooke","B) Siegfried Sassoon","C) Wilfred Owen","D) Edward Thomas"],"ans":"C","difficulty":"easy"},
    {"id":33,"topic":"American Literature","subtopic":"19th Century","q":"\"Call me Ishmael\" begins the novel by:","opts":["A) Mark Twain","B) Nathaniel Hawthorne","C) Herman Melville","D) Henry James"],"ans":"C","difficulty":"easy"},
    {"id":34,"topic":"Indian Literature","subtopic":"Fiction","q":"The God of Small Things (1997) was written by:","opts":["A) Kiran Desai","B) Anita Desai","C) Arundhati Roy","D) Shashi Deshpande"],"ans":"C","difficulty":"easy"},
    {"id":35,"topic":"Indian Literature","subtopic":"Poetry","q":"Gitanjali, translated into English by its author, was written by:","opts":["A) Sri Aurobindo","B) Sarojini Naidu","C) Rabindranath Tagore","D) Michael Madhusudan Dutt"],"ans":"C","difficulty":"easy"},
    {"id":36,"topic":"Indian Literature","subtopic":"Drama","q":"Ghashiram Kotwal was written by:","opts":["A) Girish Karnad","B) Vijay Tendulkar","C) Mahesh Dattani","D) Badal Sircar"],"ans":"B","difficulty":"medium"},
    {"id":37,"topic":"Indian Literature","subtopic":"Drama","q":"Tale Danda by Girish Karnad dramatises conflict between:","opts":["A) Mughal court factions","B) Brahminical orthodoxy and Veerashaiva reform","C) Hindu and Muslim communities","D) Colonial rulers and nationalists"],"ans":"B","difficulty":"medium"},
    {"id":38,"topic":"World Literature","subtopic":"African Literature","q":"Nervous Conditions (1988) was written by:","opts":["A) Chimamanda Ngozi Adichie","B) Tsitsi Dangarembga","C) Buchi Emecheta","D) Grace Ogot"],"ans":"B","difficulty":"hard"},
    {"id":39,"topic":"World Literature","subtopic":"Dystopian","q":"The dystopian novel We (1924), influencing Brave New World and 1984, was written by:","opts":["A) Aldous Huxley","B) George Orwell","C) Yevgeny Zamyatin","D) Arthur Koestler"],"ans":"C","difficulty":"hard"},
    {"id":40,"topic":"British Literature","subtopic":"Modernism","q":"Molly Bloom's famous soliloquy appears in:","opts":["A) The Waves","B) Mrs Dalloway","C) Ulysses","D) To the Lighthouse"],"ans":"C","difficulty":"easy"},
    {"id":41,"topic":"Linguistics","subtopic":"Rhetoric","q":"Repetition of a phrase at the start of successive clauses is called:","opts":["A) Epistrophe","B) Anaphora","C) Chiasmus","D) Anadiplosis"],"ans":"B","difficulty":"medium"},
    {"id":42,"topic":"Linguistics","subtopic":"Semantics","q":"Meaning improvement over time (e.g. 'knight': servant → noble warrior) is called:","opts":["A) Pejoration","B) Amelioration","C) Broadening","D) Narrowing"],"ans":"B","difficulty":"hard"},
    {"id":43,"topic":"British Literature","subtopic":"Renaissance","q":"Shakespeare's First Folio was published in:","opts":["A) 1609","B) 1616","C) 1623","D) 1631"],"ans":"C","difficulty":"medium"},
    {"id":44,"topic":"Literary Theory","subtopic":"New Historicism","q":"'Thick description', adopted by literary critics, was coined by:","opts":["A) Clifford Geertz","B) Stephen Greenblatt","C) Raymond Williams","D) Fredric Jameson"],"ans":"A","difficulty":"hard"},
    {"id":45,"topic":"British Literature","subtopic":"Victorian","q":"Vanity Fair's subtitle is:","opts":["A) A Novel of Manners","B) A Novel without a Hero","C) A Domestic Romance","D) A Story of English Life"],"ans":"B","difficulty":"medium"},
    {"id":46,"topic":"Literary Theory","subtopic":"Postcolonialism","q":"'Can the Subaltern Speak?' (1988) was written by:","opts":["A) Homi Bhabha","B) Edward Said","C) Frantz Fanon","D) Gayatri Chakravorty Spivak"],"ans":"D","difficulty":"medium"},
    {"id":47,"topic":"Linguistics","subtopic":"Language Teaching","q":"The Natural Approach emphasises:","opts":["A) Grammar rules first","B) Listening and speaking before reading/writing","C) Translation as primary method","D) Drilling and pattern repetition"],"ans":"B","difficulty":"medium"},
    {"id":48,"topic":"British Literature","subtopic":"Victorian","q":"The fictional Wessex in Hardy's novels is modelled on:","opts":["A) London","B) Canterbury","C) Cotswolds","D) Dorset"],"ans":"D","difficulty":"medium"},
    {"id":49,"topic":"Literary Theory","subtopic":"Classical","q":"Aristotle's term for the protagonist's fatal flaw:","opts":["A) Anagnorisis","B) Peripeteia","C) Catharsis","D) Hamartia"],"ans":"D","difficulty":"medium"},
    {"id":50,"topic":"British Literature","subtopic":"Renaissance","q":"Which character in Othello engineers the hero's destruction?","opts":["A) Cassio","B) Roderigo","C) Iago","D) Brabantio"],"ans":"C","difficulty":"easy"},
    {"id":51,"topic":"British Literature","subtopic":"18th Century","q":"Drapier's Letters belong to the Irish phase of:","opts":["A) Addison","B) Steele","C) Swift","D) Pope"],"ans":"C","difficulty":"medium"},
    {"id":52,"topic":"Linguistics","subtopic":"Morphology","q":"New words formed by combining two free morphemes is called:","opts":["A) Affixation","B) Compounding","C) Conversion","D) Blending"],"ans":"B","difficulty":"easy"},
    {"id":53,"topic":"Indian Literature","subtopic":"Drama","q":"On a Muggy Night in Mumbai was written by:","opts":["A) Vijay Tendulkar","B) Girish Karnad","C) Mahesh Dattani","D) Badal Sircar"],"ans":"C","difficulty":"medium"},
    {"id":54,"topic":"World Literature","subtopic":"Poetry","q":"Des Imagistes (1914), promoting Imagism, was edited by:","opts":["A) T.S. Eliot","B) Ezra Pound","C) Amy Lowell","D) H.D."],"ans":"B","difficulty":"medium"},
    {"id":55,"topic":"British Literature","subtopic":"Medieval","q":"Chaucer's Troilus and Criseyde is set during:","opts":["A) The Hundred Years' War","B) The Wars of the Roses","C) The Trojan War","D) The Crusades"],"ans":"C","difficulty":"medium"},
    {"id":56,"topic":"Literary Theory","subtopic":"Marxism","q":"'Cultural Materialism' is primarily associated with:","opts":["A) Stephen Greenblatt","B) Raymond Williams","C) Terry Eagleton","D) Fredric Jameson"],"ans":"B","difficulty":"medium"},
    {"id":57,"topic":"British Literature","subtopic":"Victorian","q":"The Yellow Book quarterly is associated with:","opts":["A) Imagist movement","B) Aesthetic/Decadent movement of the 1890s","C) Pre-Raphaelite Brotherhood","D) Bloomsbury Group"],"ans":"B","difficulty":"hard"},
    {"id":58,"topic":"Literary Theory","subtopic":"New Historicism","q":"New Historicism is primarily associated with:","opts":["A) Raymond Williams","B) Stephen Greenblatt","C) Terry Eagleton","D) Fredric Jameson"],"ans":"B","difficulty":"medium"},
    {"id":59,"topic":"British Literature","subtopic":"Romanticism","q":"Keats expressed the poet's temperament through:","opts":["A) Negative Capability","B) Willing Suspension of Disbelief","C) Objective Correlative","D) Poetic Justice"],"ans":"A","difficulty":"easy"},
    {"id":60,"topic":"Linguistics","subtopic":"Sociolinguistics","q":"'Received Pronunciation' (RP) is best described as:","opts":["A) Most widely spoken accent in England","B) The oldest English accent","C) The prestige accent of British English","D) The accent of the working class"],"ans":"C","difficulty":"medium"},
    # extra questions
    {"id":61,"topic":"British Literature","subtopic":"Victorian","q":"Far from the Madding Crowd was written by:","opts":["A) George Eliot","B) Elizabeth Gaskell","C) Thomas Hardy","D) George Meredith"],"ans":"C","difficulty":"easy"},
    {"id":62,"topic":"American Literature","subtopic":"Fiction","q":"The Scarlet Letter was written by:","opts":["A) Herman Melville","B) Nathaniel Hawthorne","C) Henry James","D) Mark Twain"],"ans":"B","difficulty":"easy"},
    {"id":63,"topic":"British Literature","subtopic":"Romanticism","q":"'Ode to a Nightingale' was written by:","opts":["A) Wordsworth","B) Shelley","C) Byron","D) Keats"],"ans":"D","difficulty":"easy"},
    {"id":64,"topic":"Literary Theory","subtopic":"Postcolonialism","q":"The Location of Culture (1994) was written by:","opts":["A) Gayatri Spivak","B) Homi Bhabha","C) Edward Said","D) Frantz Fanon"],"ans":"B","difficulty":"medium"},
    {"id":65,"topic":"Indian Literature","subtopic":"Fiction","q":"Midnight's Children (1981) was written by:","opts":["A) Vikram Seth","B) Amitav Ghosh","C) Salman Rushdie","D) Rohinton Mistry"],"ans":"C","difficulty":"easy"},
    {"id":66,"topic":"Linguistics","subtopic":"Pragmatics","q":"Grice's Cooperative Principle involves the maxims of:","opts":["A) Quality, Quantity, Relation, Manner","B) Voice, Tense, Aspect, Mood","C) Phonology, Syntax, Semantics, Pragmatics","D) Register, Dialect, Accent, Idiolect"],"ans":"A","difficulty":"medium"},
    {"id":67,"topic":"British Literature","subtopic":"18th Century","q":"The Rape of the Lock is a mock-epic poem by:","opts":["A) John Dryden","B) Alexander Pope","C) Jonathan Swift","D) Samuel Johnson"],"ans":"B","difficulty":"easy"},
    {"id":68,"topic":"American Literature","subtopic":"Poetry","q":"'The Waste Land' (1922) was written by:","opts":["A) Ezra Pound","B) W.B. Yeats","C) T.S. Eliot","D) Wallace Stevens"],"ans":"C","difficulty":"easy"},
    {"id":69,"topic":"Literary Theory","subtopic":"Criticism","q":"Seven Types of Ambiguity was written by:","opts":["A) I.A. Richards","B) F.R. Leavis","C) William Empson","D) Cleanth Brooks"],"ans":"C","difficulty":"medium"},
    {"id":70,"topic":"World Literature","subtopic":"African Literature","q":"Death and the King's Horseman was written by:","opts":["A) Chinua Achebe","B) Wole Soyinka","C) Ngugi wa Thiong'o","D) Ben Okri"],"ans":"B","difficulty":"medium"},
    {"id":71,"topic":"British Literature","subtopic":"Medieval","q":"Piers Plowman was written by:","opts":["A) Geoffrey Chaucer","B) John Gower","C) William Langland","D) Anonymous"],"ans":"C","difficulty":"medium"},
    {"id":72,"topic":"Linguistics","subtopic":"Historical Linguistics","q":"The Great Vowel Shift occurred approximately:","opts":["A) 800–1100 AD","B) 1100–1300","C) 1400–1700","D) 1700–1900"],"ans":"C","difficulty":"medium"},
    {"id":73,"topic":"Indian Literature","subtopic":"Poetry","q":"The Indian poet known for 'The Snake' and 'A River' is:","opts":["A) Nissim Ezekiel","B) A.K. Ramanujan","C) Dom Moraes","D) Keki Daruwalla"],"ans":"B","difficulty":"medium"},
    {"id":74,"topic":"British Literature","subtopic":"Drama","q":"Look Back in Anger (1956) was written by:","opts":["A) Harold Pinter","B) John Osborne","C) Arnold Wesker","D) Tom Stoppard"],"ans":"B","difficulty":"easy"},
    {"id":75,"topic":"Literary Theory","subtopic":"Criticism","q":"The Well Wrought Urn (1947) was written by:","opts":["A) I.A. Richards","B) William Empson","C) Cleanth Brooks","D) John Crowe Ransom"],"ans":"C","difficulty":"hard"},
]

TOPICS = sorted(set(q["topic"] for q in QUESTION_BANK))
DIFFICULTIES = ["easy","medium","hard"]

# ══════════════════════════════════════════════════════════════════════════════
#  KNOWLEDGE BASE  (used in Notes / Timeline / Quotes / Authors sections)
# ══════════════════════════════════════════════════════════════════════════════
TIMELINE_DATA = [
    ("c.700","Beowulf composed (Old English alliterative epic)"),
    ("1066","Norman Conquest → French influence on English language"),
    ("c.1387","Chaucer begins The Canterbury Tales"),
    ("1476","Caxton sets up first English printing press at Westminster"),
    ("1516","Thomas More's Utopia published (in Latin)"),
    ("1590","Spenser's The Faerie Queene (Books I–III)"),
    ("1590","Shakespeare's earliest plays (Henry VI trilogy)"),
    ("1604","Marlowe's Doctor Faustus published"),
    ("1611","King James Bible published"),
    ("1623","Shakespeare's First Folio published"),
    ("1667","Milton's Paradise Lost published (10 books)"),
    ("1719","Defoe's Robinson Crusoe"),
    ("1726","Swift's Gulliver's Travels"),
    ("1749","Fielding's Tom Jones"),
    ("1755","Johnson's Dictionary of the English Language"),
    ("1791","Boswell's Life of Samuel Johnson"),
    ("1798","Wordsworth & Coleridge: Lyrical Ballads"),
    ("1813","Austen's Pride and Prejudice"),
    ("1818","Mary Shelley's Frankenstein; Keats's Endymion"),
    ("1830","Tennyson's Poems, Chiefly Lyrical"),
    ("1847","Charlotte Brontë: Jane Eyre; Emily Brontë: Wuthering Heights"),
    ("1851","Melville's Moby-Dick"),
    ("1859","Darwin's On the Origin of Species; Tennyson's Idylls of the King"),
    ("1861","Dickens's Great Expectations"),
    ("1871","George Eliot's Middlemarch"),
    ("1890","James Frazer's The Golden Bough"),
    ("1895","Thomas Hardy's Jude the Obscure"),
    ("1898","Henry James's The Turn of the Screw"),
    ("1900","Freud's The Interpretation of Dreams"),
    ("1902","Conrad's Heart of Darkness"),
    ("1913","D.H. Lawrence's Sons and Lovers"),
    ("1916","Saussure's Course in General Linguistics (posthumous)"),
    ("1922","T.S. Eliot's The Waste Land; Joyce's Ulysses"),
    ("1924","E.M. Forster's A Passage to India"),
    ("1925","Woolf's Mrs Dalloway; Fitzgerald's The Great Gatsby"),
    ("1928","Woolf's Orlando"),
    ("1929","Woolf's A Room of One's Own"),
    ("1938","Beckett meets Joyce in Paris"),
    ("1945","Orwell's Animal Farm"),
    ("1949","Orwell's Nineteen Eighty-Four; Simone de Beauvoir's The Second Sex"),
    ("1951","Beckett's Waiting for Godot (written)"),
    ("1953","Beckett's Waiting for Godot (first performed, Paris)"),
    ("1956","John Osborne's Look Back in Anger"),
    ("1958","Achebe's Things Fall Apart"),
    ("1963","Betty Friedan's The Feminine Mystique"),
    ("1967","Derrida's Of Grammatology; Roland Barthes' 'Death of the Author'"),
    ("1978","Said's Orientalism"),
    ("1981","Rushdie's Midnight's Children (Booker Prize)"),
    ("1984","Spivak translates Derrida's Of Grammatology"),
    ("1988","Spivak's 'Can the Subaltern Speak?'; Toni Morrison's Beloved (Pulitzer)"),
    ("1994","Homi Bhabha's The Location of Culture"),
    ("1997","Arundhati Roy's The God of Small Things (Booker Prize)"),
    ("2003","J.M. Coetzee wins Nobel Prize in Literature"),
    ("2022","Geetanjali Shree's Tomb of Sand wins International Booker Prize"),
]

IMPORTANT_QUOTES = [
    {"quote":"Beauty is truth, truth beauty, — that is all ye know on earth, and all ye need to know.","author":"John Keats","work":"Ode on a Grecian Urn (1819)","note":"Closing lines; often cited in discussions of aestheticism."},
    {"quote":"To be, or not to be, that is the question.","author":"William Shakespeare","work":"Hamlet, Act III Scene I","note":"Hamlet's soliloquy on existence and inaction."},
    {"quote":"It was the best of times, it was the worst of times.","author":"Charles Dickens","work":"A Tale of Two Cities (1859)","note":"Famous opening; contrasts pre-Revolutionary France and England."},
    {"quote":"Things fall apart; the centre cannot hold.","author":"W.B. Yeats","work":"'The Second Coming' (1919)","note":"Also the source of Achebe's title Things Fall Apart."},
    {"quote":"April is the cruellest month, breeding / Lilacs out of the dead land.","author":"T.S. Eliot","work":"The Waste Land (1922)","note":"Opening lines; alludes to Chaucer's Canterbury Tales."},
    {"quote":"I am large, I contain multitudes.","author":"Walt Whitman","work":"'Song of Myself' (1855/1881)","note":"Whitman's celebration of democratic selfhood."},
    {"quote":"No man is an island, entire of itself.","author":"John Donne","work":"Meditation XVII (Devotions Upon Emergent Occasions, 1624)","note":"Source of Hemingway's title For Whom the Bell Tolls."},
    {"quote":"Whatever our souls are made of, his and mine are the same.","author":"Emily Brontë","work":"Wuthering Heights (1847)","note":"Catherine's famous declaration about Heathcliff."},
    {"quote":"The medium is the message.","author":"Marshall McLuhan","work":"Understanding Media (1964)","note":"Core concept in media theory; often misattributed."},
    {"quote":"One is not born, but rather becomes, a woman.","author":"Simone de Beauvoir","work":"The Second Sex (1949)","note":"Foundational statement of existentialist feminism."},
    {"quote":"The personal is political.","author":"Carol Hanisch","work":"'The Personal Is Political' (1969)","note":"Slogan of second-wave feminism; often misattributed to others."},
    {"quote":"I am not what I am.","author":"William Shakespeare","work":"Othello, Act I Scene I","note":"Iago's declaration of his deceptive nature."},
    {"quote":"Gather ye rosebuds while ye may, Old Time is still a-flying.","author":"Robert Herrick","work":"'To the Virgins, to Make Much of Time' (1648)","note":"Carpe diem theme; echoes Horace's Odes."},
    {"quote":"Do I dare / Disturb the universe?","author":"T.S. Eliot","work":"'The Love Song of J. Alfred Prufrock' (1915)","note":"Prufrock's paralytic self-questioning."},
    {"quote":"The owl of Minerva spreads its wings only with the falling of the dusk.","author":"G.W.F. Hegel","work":"Philosophy of Right (1820)","note":"On the retrospective nature of philosophy; cited in literary theory."},
]

AUTHOR_PROFILES = [
    {"name":"Geoffrey Chaucer","dates":"c.1343–1400","period":"Medieval","bio":"Father of English literature. Civil servant, diplomat, and poet who wrote in Middle English. Influenced by Italian writers Boccaccio and Petrarch.","works":"The Canterbury Tales, Troilus and Criseyde, The Book of the Duchess, The Parliament of Fowls","note":"His use of the vernacular established English as a literary language."},
    {"name":"William Shakespeare","dates":"1564–1616","period":"Renaissance/Elizabethan","bio":"Playwright and poet, born in Stratford-upon-Avon. Wrote 37 plays, 154 sonnets, and two long narrative poems. His works were first collected in the First Folio (1623).","works":"Hamlet, Othello, King Lear, Macbeth, A Midsummer Night's Dream, The Tempest, Sonnets","note":"Often called the Bard; coined over 1,700 English words."},
    {"name":"John Milton","dates":"1608–1674","period":"Renaissance/Puritan","bio":"Poet and political writer. Composed Paradise Lost after going blind. A fierce defender of civil liberties and press freedom in Areopagitica.","works":"Paradise Lost (1667), Paradise Regained, Samson Agonistes, Lycidas, L'Allegro, Il Penseroso","note":"Paradise Lost is considered the greatest epic in English."},
    {"name":"Jane Austen","dates":"1775–1817","period":"Romantic/Regency","bio":"Novelist known for irony, social commentary, and the marriage plot. Published anonymously during her lifetime.","works":"Sense and Sensibility, Pride and Prejudice, Emma, Mansfield Park, Northanger Abbey, Persuasion","note":"Pioneer of free indirect discourse as a narrative technique."},
    {"name":"Charles Dickens","dates":"1812–1870","period":"Victorian","bio":"Most popular novelist of the Victorian era. Championed the poor and criticised industrialisation and workhouses. Began career as a journalist.","works":"Oliver Twist, David Copperfield, Bleak House, Great Expectations, A Tale of Two Cities, Hard Times","note":"Serialised novels made him accessible to the working class."},
    {"name":"T.S. Eliot","dates":"1888–1965","period":"Modernism","bio":"Born in St Louis, Missouri; became a British citizen (1927). Nobel Prize 1948. Key critical concept: 'objective correlative'.","works":"The Waste Land, The Love Song of J. Alfred Prufrock, Four Quartets, Murder in the Cathedral, The Sacred Wood","note":"Coined 'dissociation of sensibility' and 'objective correlative'."},
    {"id":"woolf","name":"Virginia Woolf","dates":"1882–1941","period":"Modernism","bio":"Co-founded Hogarth Press with husband Leonard Woolf. Central member of Bloomsbury Group. Pioneer of stream-of-consciousness technique.","works":"Mrs Dalloway, To the Lighthouse, The Waves, Orlando, A Room of One's Own","note":"Feminist critic; argued women need money and privacy to write."},
    {"name":"James Joyce","dates":"1882–1941","period":"Modernism","bio":"Irish novelist who spent most of his life in continental Europe. Revolutionised the novel with stream of consciousness and linguistic experimentation.","works":"Dubliners, A Portrait of the Artist as a Young Man, Ulysses, Finnegans Wake","note":"Ulysses is ranked #1 on most lists of greatest English-language novels."},
    {"name":"Rabindranath Tagore","dates":"1861–1941","period":"Indian Modernism","bio":"First Asian to win the Nobel Prize in Literature (1913). Bengali polymath: poet, novelist, playwright, composer, visual artist. Founded Visva-Bharati University.","works":"Gitanjali, Gora, The Home and the World, Chokher Bali, Post Office","note":"Translated his own Bengali Gitanjali into English."},
    {"name":"Chinua Achebe","dates":"1930–2013","period":"Postcolonial","bio":"Nigerian novelist, often called the father of African literature in English. Wrote Things Fall Apart as a counter-narrative to Conrad's Heart of Darkness.","works":"Things Fall Apart, Arrow of God, No Longer at Ease, A Man of the People, Anthills of the Savannah","note":"Things Fall Apart has sold over 20 million copies worldwide."},
    {"name":"Salman Rushdie","dates":"1947–","period":"Postcolonial/Contemporary","bio":"Born in Mumbai; educated at Cambridge. Midnight's Children won the Booker Prize (1981) and the Booker of Bookers. The Satanic Verses triggered a fatwa in 1989.","works":"Midnight's Children, Shame, The Satanic Verses, The Moor's Last Sigh, The Ground Beneath Her Feet","note":"Master of magical realism in the postcolonial tradition."},
    {"name":"Samuel Beckett","dates":"1906–1989","period":"Absurdism/Modernism","bio":"Irish playwright and novelist, lived in Paris. Friend and secretary to James Joyce. Nobel Prize 1969. His drama of 'nothing' transformed 20th-century theatre.","works":"Waiting for Godot, Endgame, Happy Days, Krapp's Last Tape, Murphy, Molloy","note":"Wrote in both English and French, often translating his own work."},
]

THEORY_NOTES = {
    "New Criticism": {
        "summary": "American formalist movement (1930s–60s). Focus on the text itself, not biographical or historical context. Key concept: the 'well-wrought urn' (Cleanth Brooks).",
        "key_figures": "I.A. Richards, William Empson, Cleanth Brooks, John Crowe Ransom, Allen Tate, W.K. Wimsatt, Monroe Beardsley",
        "key_concepts": "Intentional fallacy, Affective fallacy, Ambiguity, Irony, Tension, Paradox, Organic unity",
        "key_texts": "Seven Types of Ambiguity (Empson, 1930), The Well Wrought Urn (Brooks, 1947), Understanding Poetry (Brooks & Warren, 1938)",
    },
    "Structuralism": {
        "summary": "Applied Saussurean linguistics to literature and culture. Literature as a system of signs governed by codes and conventions.",
        "key_figures": "Ferdinand de Saussure, Claude Lévi-Strauss, Roland Barthes (early), A.J. Greimas, Gerard Genette",
        "key_concepts": "Langue/Parole, Signifier/Signified, Binary oppositions, Narrative grammar, Synchronic vs diachronic",
        "key_texts": "Course in General Linguistics (Saussure, 1916), Mythologies (Barthes, 1957), Morphology of the Folktale (Propp, 1928)",
    },
    "Deconstruction": {
        "summary": "Post-structuralist critique showing how texts undermine their own claims to stable meaning. Texts are always already divided and deferred.",
        "key_figures": "Jacques Derrida, Paul de Man, J. Hillis Miller, Geoffrey Hartman, Barbara Johnson",
        "key_concepts": "Différance, Logocentrism, Binary oppositions, Trace, Supplement, Aporia, Iterability",
        "key_texts": "Of Grammatology (Derrida, 1967), Writing and Difference (1967), Blindness and Insight (de Man, 1971)",
    },
    "Postcolonialism": {
        "summary": "Examines the cultural legacies of colonialism and imperialism. Critiques Eurocentrism and recovers subaltern voices and perspectives.",
        "key_figures": "Edward Said, Homi Bhabha, Gayatri Chakravorty Spivak, Frantz Fanon, Chinua Achebe",
        "key_concepts": "Orientalism, Hybridity, Mimicry, Ambivalence, Subaltern, The Other, Third Space",
        "key_texts": "Orientalism (Said, 1978), The Location of Culture (Bhabha, 1994), Can the Subaltern Speak? (Spivak, 1988), The Wretched of the Earth (Fanon, 1961)",
    },
    "Feminist Criticism": {
        "summary": "Examines how gender shapes literary production, representation, and reception. From images-of-women criticism to écriture féminine and gender performativity.",
        "key_figures": "Elaine Showalter, Hélène Cixous, Julia Kristeva, Luce Irigaray, Sandra Gilbert & Susan Gubar, Judith Butler",
        "key_concepts": "Gynocriticism, Écriture féminine, Semiotic/Symbolic, Abjection, Performativity, Anxiety of authorship",
        "key_texts": "A Room of One's Own (Woolf, 1929), The Second Sex (Beauvoir, 1949), The Madwoman in the Attic (Gilbert & Gubar, 1979), Gender Trouble (Butler, 1990)",
    },
    "Marxist Criticism": {
        "summary": "Analyses literature through the lens of class struggle, ideology, and the material conditions of production. Literature reflects and reproduces ideological formations.",
        "key_figures": "Karl Marx, Friedrich Engels, Georg Lukács, Antonio Gramsci, Louis Althusser, Raymond Williams, Terry Eagleton, Fredric Jameson",
        "key_concepts": "Base/Superstructure, Ideology, Hegemony, Ideological State Apparatus, Reification, Commodity fetishism, Cultural materialism",
        "key_texts": "Ideology and Ideological State Apparatuses (Althusser, 1970), Marxism and Literature (Williams, 1977), The Political Unconscious (Jameson, 1981)",
    },
    "New Historicism": {
        "summary": "Reads literary texts alongside non-literary texts of the same period. History is textual; texts circulate power. Developed in Renaissance studies.",
        "key_figures": "Stephen Greenblatt, Louis Montrose, Catherine Gallagher, Jonathan Goldberg",
        "key_concepts": "Thick description (from Clifford Geertz), Circulation of social energy, Subversion and containment, Anecdote",
        "key_texts": "Renaissance Self-Fashioning (Greenblatt, 1980), Shakespearean Negotiations (Greenblatt, 1988)",
    },
    "Psychoanalytic Criticism": {
        "summary": "Applies Freudian and Lacanian concepts to texts, authors, and readers. Reads the unconscious of the text.",
        "key_figures": "Sigmund Freud, Jacques Lacan, Harold Bloom, Julia Kristeva, Norman Holland",
        "key_concepts": "The unconscious, Repression, Oedipus complex, The uncanny, Mirror stage, Imaginary/Symbolic/Real, The gaze, Anxiety of influence",
        "key_texts": "The Interpretation of Dreams (Freud, 1900), Écrits (Lacan, 1966), The Anxiety of Influence (Bloom, 1973)",
    },
}

LINGUISTICS_NOTES = {
    "Phonetics & Phonology": {
        "summary": "Phonetics studies the physical sounds of speech; phonology studies how sounds function as a system in a particular language.",
        "key_concepts": "IPA (International Phonetic Alphabet), Place of articulation (bilabial, alveolar, velar, etc.), Manner of articulation (plosive, fricative, nasal, lateral, approximant), Voicing (voiced vs voiceless), Phoneme, Allophone, Minimal pair, Syllable structure (onset–nucleus–coda), Stress, Intonation",
        "examples": "English has ~44 phonemes but 26 letters. /p/ and /b/ are a minimal pair (pin vs bin). /l/ and /r/ are allophones in some languages.",
    },
    "Morphology": {
        "summary": "The study of word structure and word formation processes.",
        "key_concepts": "Morpheme (free vs bound), Prefix, Suffix, Infix, Root, Stem, Inflection, Derivation, Compounding, Blending (smoke+fog=smog), Clipping (advertisement→ad), Acronym, Back-formation, Conversion (zero-derivation)",
        "examples": "Un-kind-ness has 3 morphemes. 'Brunch' is a blend of breakfast+lunch. 'Google' became a verb by conversion.",
    },
    "Semantics & Pragmatics": {
        "summary": "Semantics is the study of meaning in language; pragmatics is the study of meaning in context.",
        "key_concepts": "Sense vs reference, Synonymy, Antonymy, Hyponymy, Polysemy, Ambiguity, Semantic change (amelioration, pejoration, broadening, narrowing), Speech acts (Austin/Searle), Implicature (Grice), Cooperative Principle (Quality, Quantity, Relation, Manner), Context",
        "examples": "Grice's maxims: 'Can you pass the salt?' is an indirect speech act (request, not question about ability).",
    },
    "Language Acquisition": {
        "summary": "The process by which humans acquire language. Two main camps: nativist and empiricist.",
        "key_concepts": "LAD (Language Acquisition Device) — Chomsky, Universal Grammar, Critical Period Hypothesis (Lenneberg), Behaviourism (Skinner) — operant conditioning, Input Hypothesis (Krashen), Zone of Proximal Development (Vygotsky), L1 vs L2 acquisition, Interlanguage",
        "examples": "Chomsky's 'colourless green ideas sleep furiously' shows grammar is independent of meaning. Children overgeneralise ('I goed') showing rule acquisition.",
    },
    "Language Teaching Methods": {
        "summary": "Various approaches to teaching second languages, each reflecting different theories of language learning.",
        "key_concepts": "Grammar-Translation Method (GTM) — oldest; Direct Method — immersion; Audio-Lingual Method — drilling; Communicative Language Teaching (CLT) — functional; Task-Based Learning (TBL); Silent Way; Suggestopedia; Natural Approach (Krashen & Terrell)",
        "examples": "CLT asks learners to order food in a restaurant (real-world task). GTM translates Caesar's Gallic Wars.",
    },
    "Historical Linguistics": {
        "summary": "Study of how languages change over time and how they are related.",
        "key_concepts": "Proto-Indo-European (PIE), Grimm's Law (First Germanic Sound Shift), Verner's Law, Great Vowel Shift (1400–1700), Language families (Indo-European, Semitic, Sino-Tibetan), Sound change, Semantic change, Borrowing, Calque",
        "examples": "Latin pater → English father (Grimm's Law p→f). 'Beef' from French boeuf (Norman Conquest borrowing).",
    },
}

AI_TOPIC_PROMPTS = {
    "British Literature": "Old English (Beowulf), Medieval (Chaucer, Langland, Pearl-Poet), Renaissance (Shakespeare, Spenser, Marlowe, Sidney, Milton, Jonson, Donne), Restoration (Dryden, Congreve), 18th Century (Pope, Swift, Johnson, Goldsmith, Richardson, Fielding, Sterne), Romanticism (Blake, Wordsworth, Coleridge, Keats, Shelley, Byron), Victorian (Dickens, Hardy, Eliot, Tennyson, Browning, Arnold, Ruskin, Pater, Rossetti), Modernism (Woolf, Joyce, Eliot, Lawrence, Forster, Yeats, Auden, Beckett), 20th-century drama (Pinter, Osborne, Stoppard)",
    "American Literature": "Transcendentalism (Emerson, Thoreau, Whitman), 19th-century fiction (Hawthorne, Melville, Poe, Twain, Henry James), Emily Dickinson, Modernism (Hemingway, Fitzgerald, Faulkner, Steinbeck), Poetry (Frost, Stevens, Williams, Plath, Lowell), Harlem Renaissance (Hughes, Hurston), Drama (O'Neill, Miller, Tennessee Williams)",
    "Indian Literature": "Indian Writing in English (Raja Rao, Mulk Raj Anand, R.K. Narayan, Rushdie, Arundhati Roy, Vikram Seth, Amitav Ghosh, Kiran Desai, Rohinton Mistry), Indian drama (Girish Karnad, Vijay Tendulkar, Mahesh Dattani, Badal Sircar), Indian poets in English (Ezekiel, Ramanujan, Daruwalla, Kamala Das, Tagore)",
    "World Literature": "African (Achebe, Soyinka, Ngugi, Adichie, Dangarembga, Okri), Caribbean (Walcott, Rhys, Naipaul, Lamming), Canadian (Atwood, Munro, Ondaatje), Australian (Patrick White, Les Murray), Nobel laureates in Literature",
    "Literary Theory": "Classical (Aristotle, Horace), Renaissance (Sidney), Neoclassical (Dryden, Johnson), Romantic criticism (Wordsworth, Coleridge, Arnold, Pater), New Criticism (Richards, Empson, Brooks), Russian Formalism (Shklovsky, Jakobson), Structuralism (Saussure, Barthes), Deconstruction (Derrida, de Man), Marxism (Althusser, Gramsci, Williams, Eagleton), Feminism (Showalter, Cixous, Kristeva, Butler), Postcolonialism (Said, Bhabha, Spivak, Fanon), New Historicism (Greenblatt), Psychoanalytic (Freud, Lacan, Bloom)",
    "Linguistics": "Phonetics, Phonology, Morphology, Syntax, Semantics, Pragmatics (Grice), Historical linguistics (Great Vowel Shift, Grimm's Law), Sociolinguistics (register, dialect, code-switching), Language acquisition (Chomsky, Skinner, Piaget, Vygotsky), Language teaching methods (GTM, Direct, Audio-Lingual, CLT, TBL)",
}
SUBTOPIC_MAP = {
    "British Literature":["Old English","Medieval","Renaissance","Restoration","18th Century","Romanticism","Victorian","Modernism","20th Century Drama","Contemporary"],
    "American Literature":["Colonial","Transcendentalism","19th Century Fiction","Poetry","Modernism","Harlem Renaissance","Drama","Contemporary"],
    "Indian Literature":["Fiction","Poetry","Drama","Partition Literature","Dalit Literature","Postcolonial Fiction"],
    "World Literature":["African Literature","Caribbean Literature","Australian Literature","Canadian Literature","Nobel Laureates"],
    "Literary Theory":["Classical","New Criticism","Structuralism","Poststructuralism","Deconstruction","Feminism","Marxism","Postcolonialism","New Historicism","Psychoanalytic Criticism"],
    "Linguistics":["Phonetics","Phonology","Morphology","Syntax","Semantics","Pragmatics","Language Acquisition","Sociolinguistics","Language Teaching","Historical Linguistics"],
}
QUESTION_TYPES=[
    "identification (who wrote / who said / which work)",
    "definition of a literary or linguistic term",
    "chronological ordering of works or literary periods",
    "true/false statement pairs (Statement 1 / Statement 2 format)",
    "match List I with List II (4 items each side)",
    "complete the famous quote",
    "multiple works by the same author",
    "which literary period or movement does this belong to",
    "character identification",
    "identify the correct or incorrect critical statement",
]
ANGLES=[
    "focusing on dates and first publication facts",
    "about key quotations and their sources",
    "from a literary history and periodisation angle",
    "about critical reception and famous critics' views",
    "about influence, intertextuality, and literary debts",
    "about narrative technique, point of view, or form",
    "about thematic concerns, symbols, and imagery",
    "about the author's biography",
    "about genre classifications and formal features",
    "about theoretical frameworks and schools of thought",
]

# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
def init_state():
    defs = {"api_key":"","ai_questions":[],"quiz_questions":[],
            "current_idx":0,"answers":{},"quiz_started":False,
            "quiz_finished":False,"score":0,"page":"home",
            "total_attempted":0,"total_correct":0,
            "topic_stats":{},"difficulty_stats":{},
            "streak":0,"best_streak":0}
    for k,v in defs.items():
        if k not in st.session_state: st.session_state[k]=v
init_state()

def all_questions(): return QUESTION_BANK + st.session_state.ai_questions

def start_quiz(topic_filter=None,difficulty_filter=None,count=20):
    pool=all_questions()
    if topic_filter: pool=[q for q in pool if q["topic"] in topic_filter]
    if difficulty_filter: pool=[q for q in pool if q["difficulty"] in difficulty_filter]
    random.shuffle(pool)
    st.session_state.quiz_questions=pool[:count]
    st.session_state.current_idx=0; st.session_state.answers={}
    st.session_state.quiz_started=True; st.session_state.quiz_finished=False
    st.session_state.score=0; st.session_state.streak=0

def submit_answer(q_id,letter):
    q=next((x for x in st.session_state.quiz_questions if x["id"]==q_id),None)
    if q is None or q_id in st.session_state.answers: return None
    ok=letter==q["ans"]
    st.session_state.answers[q_id]={"selected":letter,"correct":q["ans"],"is_correct":ok}
    st.session_state.total_attempted+=1
    t=q.get("topic","Other"); d=q.get("difficulty","medium")
    for store,key in [(st.session_state.topic_stats,t),(st.session_state.difficulty_stats,d)]:
        if key not in store: store[key]={"attempted":0,"correct":0}
        store[key]["attempted"]+=1
    if ok:
        st.session_state.total_correct+=1; st.session_state.score+=1
        st.session_state.streak+=1
        st.session_state.topic_stats[t]["correct"]+=1
        st.session_state.difficulty_stats[d]["correct"]+=1
        if st.session_state.streak>st.session_state.best_streak:
            st.session_state.best_streak=st.session_state.streak
    else: st.session_state.streak=0
    return ok

def reset_quiz():
    st.session_state.quiz_started=False; st.session_state.quiz_finished=False
    st.session_state.answers={}; st.session_state.quiz_questions=[]
    st.session_state.current_idx=0; st.session_state.score=0; st.session_state.streak=0

# ══════════════════════════════════════════════════════════════════════════════
#  AI GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
def generate_questions_ai(api_key,topic,subtopic,difficulty,count=5,existing=None):
    if not existing: existing=[]
    q_type=random.choice(QUESTION_TYPES); angle=random.choice(ANGLES)
    context=AI_TOPIC_PROMPTS.get(topic,topic)
    existing_sample="\n".join(f"- {q}" for q in existing[:8])
    prompt=f"""You are an expert question setter for the Kerala SET exam in English Language and Literature.
Generate exactly {count} original MCQ questions.
SPECIFICATIONS: Topic:{topic} | Subtopic:{subtopic} | Difficulty:{difficulty}
Question type: {q_type} | Angle: {angle}
Syllabus: {context}
RULES: 4 options A) B) C) D), one correct, plausible distractors.
Do NOT repeat: {existing_sample if existing_sample else "(none)"}
Respond ONLY with valid JSON (no markdown):
{{"questions":[{{"q":"...","opts":["A) ...","B) ...","C) ...","D) ..."],"ans":"A","topic":"{topic}","subtopic":"{subtopic}","difficulty":"{difficulty}"}}]}}"""
    client=anthropic.Anthropic(api_key=api_key)
    response=client.messages.create(model="claude-opus-4-6",max_tokens=4096,
                                    messages=[{"role":"user","content":prompt}])
    raw=response.content[0].text.strip()
    m=re.search(r'\{.*\}',raw,re.DOTALL)
    if not m: return []
    data=json.loads(m.group()); questions=data.get("questions",[])
    start_id=10000+random.randint(100,89000)
    valid=[]
    for i,q in enumerate(questions):
        q["id"]=start_id+i; q["ai_generated"]=True
        if all(k in q for k in ["q","opts","ans"]) and len(q["opts"])==4 and q["ans"] in "ABCD":
            valid.append(q)
    return valid

def generate_batch(api_key,topics,difficulties,total_count,existing=None,progress_cb=None):
    if not existing: existing=[]
    combos=[(t,d) for t in topics for d in difficulties]; random.shuffle(combos)
    per=max(1,total_count//len(combos)) if combos else 1
    rem=total_count-per*len(combos); all_new=[]
    for idx,(topic,diff) in enumerate(combos):
        n=per+(1 if idx<rem else 0)
        if n<=0: continue
        subtopic=random.choice(SUBTOPIC_MAP.get(topic,[topic]))
        try:
            new_qs=generate_questions_ai(api_key,topic,subtopic,diff,count=n,existing=existing)
            all_new.extend(new_qs); existing.extend([q["q"] for q in new_qs])
        except Exception: pass
        if progress_cb: progress_cb(idx+1,len(combos))
    return all_new

# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 📚 Kerala SET")
    st.markdown("### English Literature 2026")
    st.markdown("---")
    nav=[("🏠 Home","home"),("📝 Practice Quiz","quiz"),("🤖 AI Generator","ai_gen"),
         ("📊 Analytics","analytics"),("📖 Question Bank","bank"),
         ("📜 Important Quotes","quotes"),("⏳ Literary Timeline","timeline"),
         ("👤 Author Profiles","authors"),("🧠 Theory Notes","theory"),
         ("📐 Linguistics Notes","linguistics"),("🃏 Flashcards","flashcards"),
         ("📚 Glossary","glossary"),("🏆 Nobel Prize Tracker","nobel"),
         ("📋 PYQ Analysis","pyq")]
    for label,key in nav:
        if st.button(label,key=f"nav_{key}",use_container_width=True):
            st.session_state.page=key
            if key!="quiz": reset_quiz()
            st.rerun()
    st.markdown("---")
    st.markdown("##### 🔑 Anthropic API Key")
    api_input=st.text_input("API Key",value=st.session_state.api_key,type="password",
                             label_visibility="collapsed",placeholder="sk-ant-...")
    if api_input!=st.session_state.api_key: st.session_state.api_key=api_input
    total_q=len(QUESTION_BANK)+len(st.session_state.ai_questions)
    if st.session_state.api_key:
        st.markdown(f"<small style='color:white'>✅ Key set · 🗂 {total_q} questions</small>",unsafe_allow_html=True)
    else:
        st.markdown("<small style='color:rgba(255,255,255,.6)'>Enter key for AI generation</small>",unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<small style='color:rgba(255,255,255,.5)'>NYZTrade Education · Kerala SET 2026</small>",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  HELPER: stat card
# ══════════════════════════════════════════════════════════════════════════════
def stat_cards(cards):
    html="<div class='srow'>"
    for lbl,val,cls in cards:
        html+=f"<div class='sc {cls}'><div class='lbl'>{lbl}</div><div class='val'>{val}</div></div>"
    html+="</div>"
    st.markdown(html,unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: HOME
# ══════════════════════════════════════════════════════════════════════════════
def page_home():
    st.markdown("""<div class="app-hdr"><div><h1>📚 Kerala SET Practice</h1>
    <div class="sub">English Language & Literature · AI-Powered Q&A System</div></div>
    <div class="bdg">SET 2026</div></div>""",unsafe_allow_html=True)
    ai_c=len(st.session_state.ai_questions); tot=len(QUESTION_BANK)+ai_c
    att=st.session_state.total_attempted; cor=st.session_state.total_correct
    acc=round(cor/att*100) if att else 0; bst=st.session_state.best_streak
    stat_cards([("Total Questions",tot,"sc-blue"),("Attempted",att,"sc-green"),
                ("Accuracy",f"{acc}%","sc-gold"),("Best Streak 🔥",bst,"sc-red"),
                ("AI Generated",ai_c,"sc-blue")])
    col1,col2=st.columns([2,1])
    with col1:
        st.markdown("### 🚀 Quick Start")
        c1,c2,c3=st.columns(3)
        with c1:
            if st.button("⚡ Quick 10",use_container_width=True,type="primary"):
                start_quiz(count=10); st.session_state.page="quiz"; st.rerun()
        with c2:
            if st.button("📝 Mock Test (50)",use_container_width=True):
                start_quiz(count=50); st.session_state.page="quiz"; st.rerun()
        with c3:
            if st.button("🎯 Hard Mode (20)",use_container_width=True):
                start_quiz(difficulty_filter=["hard"],count=20); st.session_state.page="quiz"; st.rerun()
        st.markdown("### 📋 Topic Coverage")
        ts=st.session_state.topic_stats
        for topic in TOPICS:
            pool=[q for q in all_questions() if q["topic"]==topic]
            att_t=ts.get(topic,{}).get("attempted",0); cor_t=ts.get(topic,{}).get("correct",0)
            acc_t=round(cor_t/att_t*100) if att_t else 0
            pct=round(att_t/len(pool)*100) if pool else 0
            st.markdown(f"""<div style="margin-bottom:9px">
            <div style="display:flex;justify-content:space-between;font-size:.83rem;margin-bottom:3px">
              <span style="font-weight:600;color:#1c1c2e">{topic}</span>
              <span style="color:#6c7a8d">{len(pool)} Qs · {att_t} done · {acc_t}% acc</span>
            </div>
            <div class="pw"><div class="pb" style="width:{pct}%"></div></div></div>""",unsafe_allow_html=True)
    with col2:
        st.markdown("### 🎯 By Topic")
        for topic in TOPICS:
            if st.button(f"📌 {topic}",key=f"ht_{topic}",use_container_width=True):
                start_quiz(topic_filter=[topic],count=15); st.session_state.page="quiz"; st.rerun()
        st.markdown("---")
        st.markdown("### 📚 Study Sections")
        study_pages=[("📜 Key Quotes","quotes"),("⏳ Timeline","timeline"),
                     ("👤 Authors","authors"),("🧠 Theory","theory"),("📐 Linguistics","linguistics")]
        for lbl,pg in study_pages:
            if st.button(lbl,key=f"home_study_{pg}",use_container_width=True):
                st.session_state.page=pg; st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: QUIZ
# ══════════════════════════════════════════════════════════════════════════════
def page_quiz():
    st.markdown("""<div class="app-hdr"><div><h1>📝 Practice Quiz</h1>
    <div class="sub">Test your Kerala SET preparation</div></div></div>""",unsafe_allow_html=True)
    if not st.session_state.quiz_started:
        st.markdown("### ⚙️ Configure Your Quiz")
        col1,col2=st.columns(2)
        with col1:
            topics_sel=st.multiselect("Topics (empty = all)",TOPICS,key="qs_t")
            diff_sel=st.multiselect("Difficulties (empty = all)",DIFFICULTIES,default=DIFFICULTIES,key="qs_d")
        with col2:
            pool_size=len([q for q in all_questions()
                           if (not topics_sel or q["topic"] in topics_sel)
                           and (not diff_sel or q["difficulty"] in diff_sel)])
            count=st.slider("Number of Questions",5,min(pool_size,120),20,key="qs_n")
            st.info(f"📦 **{pool_size}** questions match your filters")
        st.markdown("---")
        if st.button("🚀 Start Quiz",type="primary",use_container_width=True):
            if pool_size==0: st.error("No questions match — broaden filters.")
            else:
                start_quiz(topic_filter=topics_sel or None,difficulty_filter=diff_sel or None,count=count)
                st.rerun()
        return
    questions=st.session_state.quiz_questions
    if not questions: st.warning("No questions."); reset_quiz(); st.rerun(); return
    total=len(questions); answered=len(st.session_state.answers)
    if st.session_state.quiz_finished or answered>=total: _results(questions); return
    idx=st.session_state.current_idx
    if idx>=total: st.session_state.quiz_finished=True; st.rerun()
    q=questions[idx]; already=q["id"] in st.session_state.answers
    pct=int(answered/total*100)
    st.markdown(f"""<div style="display:flex;justify-content:space-between;font-size:.8rem;color:#6c7a8d;margin-bottom:4px">
    <span style="color:#6c7a8d">Question {idx+1} of {total}</span>
    <span style="color:#6c7a8d">✅ {st.session_state.score} correct · 🔥 {st.session_state.streak} streak</span></div>
    <div class="pw"><div class="pb" style="width:{pct}%"></div></div>""",unsafe_allow_html=True)
    dc=q.get("difficulty","medium")
    dc_cls={"easy":"tag-easy","medium":"tag-med","hard":"tag-hard"}.get(dc,"tag-def")
    ai_tag='<span class="tag tag-ai">🤖 AI</span>' if q.get("ai_generated") else ""
    st.markdown(f"""<div class="qcard">
    <div class="qnum">Question {idx+1}</div>
    <div class="qtags"><span class="tag tag-def">{q.get("topic","")}</span>
    <span class="tag tag-def">{q.get("subtopic","")}</span>
    <span class="tag {dc_cls}">{dc.upper()}</span>{ai_tag}</div>
    <div class="qtext">{q["q"]}</div></div>""",unsafe_allow_html=True)
    correct_letter=q["ans"]; user_ans=st.session_state.answers.get(q["id"])
    for opt in q["opts"]:
        letter=opt[0]
        if already:
            if letter==correct_letter: cls="opt correct"
            elif user_ans and letter==user_ans["selected"]: cls="opt wrong"
            else: cls="opt"
            st.markdown(f'<div class="{cls}" style="display:block;padding:.65rem 1rem;margin-bottom:.5rem;border-radius:9px;border:2px solid {"#27ae60" if letter==correct_letter else "#e74c3c" if user_ans and letter==user_ans["selected"] else "#dce3ee"};background:{"#eafaf1" if letter==correct_letter else "#fdf2f2" if user_ans and letter==user_ans["selected"] else "#f4f6fb"};color:#1c1c2e;font-size:.93rem;font-weight:{"600" if letter==correct_letter else "400"}">{opt}</div>',unsafe_allow_html=True)
        else:
            if st.button(opt,key=f"o_{q['id']}_{letter}",use_container_width=True):
                submit_answer(q["id"],letter); st.rerun()
    if already:
        co=next(o for o in q["opts"] if o[0]==correct_letter)
        if user_ans["is_correct"]: st.success(f"✅ Correct! **{co}**")
        else:
            sel=next((o for o in q["opts"] if o[0]==user_ans["selected"]),"")
            st.error(f"❌ You chose **{sel}** · Correct: **{co}**")
        _,mid,_=st.columns([1,2,1])
        with mid:
            lbl="Next ➡️" if idx<total-1 else "Finish 🏁"
            if st.button(lbl,type="primary",use_container_width=True,key="next_btn"):
                if idx<total-1: st.session_state.current_idx+=1; st.rerun()
                else: st.session_state.quiz_finished=True; st.rerun()
    st.markdown("---")
    if st.button("🔄 Restart",key="restart"): reset_quiz(); st.rerun()

def _results(questions):
    total=len(questions); score=st.session_state.score
    pct=round(score/total*100) if total else 0
    grade=("Excellent! 🏆" if pct>=80 else "Good 👍" if pct>=60 else "Needs Improvement 📖" if pct>=40 else "Keep Studying 💪")
    st.markdown(f"""<div class="rcard"><div class="rscore">{score}/{total}</div>
    <div class="rtotal">Questions Correct</div><div class="rgrade">{grade} — {pct}%</div></div>""",unsafe_allow_html=True)
    st.markdown("### 📊 Topic Breakdown")
    tr={}
    for q in questions:
        t=q.get("topic","Other")
        if t not in tr: tr[t]={"a":0,"c":0}
        if q["id"] in st.session_state.answers:
            tr[t]["a"]+=1
            if st.session_state.answers[q["id"]]["is_correct"]: tr[t]["c"]+=1
    for topic,s in tr.items():
        acc=round(s["c"]/s["a"]*100) if s["a"] else 0
        col="#27ae60" if acc>=70 else "#e67e22" if acc>=50 else "#e74c3c"
        st.markdown(f"""<div style="margin-bottom:9px">
        <div style="display:flex;justify-content:space-between;font-size:.83rem;margin-bottom:3px">
          <span style="font-weight:600;color:#1c1c2e">{topic}</span>
          <span style="color:#6c7a8d">{s['c']}/{s['a']} ({acc}%)</span></div>
        <div class="pw"><div class="pb" style="width:{acc}%;background:{col}"></div></div></div>""",unsafe_allow_html=True)
    wrong=[q for q in questions if q["id"] in st.session_state.answers and not st.session_state.answers[q["id"]]["is_correct"]]
    if wrong:
        with st.expander(f"📋 Review {len(wrong)} Wrong Answers"):
            for q in wrong:
                res=st.session_state.answers[q["id"]]
                co=next(o for o in q["opts"] if o[0]==q["ans"])
                yo=next((o for o in q["opts"] if o[0]==res["selected"]),"–")
                st.markdown(f"""<div class="wrong-box">
                <div class="wq">{q["q"]}</div>
                <div class="wy">❌ You chose: {yo}</div>
                <div class="wc">✅ Correct answer: {co}</div></div>""",unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        if st.button("🔄 New Quiz",type="primary",use_container_width=True): reset_quiz(); st.rerun()
    with c2:
        if st.button("🏠 Home",use_container_width=True):
            reset_quiz(); st.session_state.page="home"; st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: AI GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
def page_ai_gen():
    st.markdown("""<div class="app-hdr"><div><h1>🤖 AI Question Generator</h1>
    <div class="sub">Multiply your practice set using Claude AI</div></div>
    <div class="bdg">Powered by Claude</div></div>""",unsafe_allow_html=True)
    st.markdown("""<div class="ai-box"><h3>⚡ Permutation & Combination Engine</h3>
    <p>Selects every combination of Topic × Difficulty × Question Type × Angle, then prompts Claude
    to generate unique questions for each combo — multiplying your bank from 75 to 500+ instantly.</p></div>""",unsafe_allow_html=True)
    if not st.session_state.api_key:
        st.warning("🔑 Please enter your Anthropic API key in the sidebar.")
        st.info("Get your API key at: https://console.anthropic.com"); return
    ai_c=len(st.session_state.ai_questions)
    stat_cards([("Seed Questions",len(QUESTION_BANK),"sc-blue"),("AI Generated",ai_c,"sc-green"),
                ("Total",len(QUESTION_BANK)+ai_c,"sc-gold")])
    st.markdown("---"); st.markdown("### 🎛️ Generation Settings")
    col1,col2=st.columns(2)
    with col1:
        sel_topics=st.multiselect("Topics",TOPICS,default=TOPICS,key="gen_t")
        sel_diffs=st.multiselect("Difficulties",DIFFICULTIES,default=DIFFICULTIES,key="gen_d")
    with col2:
        n_q=st.slider("Total to generate",10,200,30,step=10,key="gen_n")
        combos=len(sel_topics)*len(sel_diffs)
        if combos:
            per=max(1,n_q//combos)
            st.info(f"📐 **{combos}** combos → ~**{per}** each → ~**{combos*per}** total")
    st.markdown("---")
    if st.button("🚀 Generate with AI",type="primary",use_container_width=True):
        if not sel_topics or not sel_diffs: st.error("Select at least one topic and difficulty."); return
        existing=[q["q"] for q in QUESTION_BANK+st.session_state.ai_questions]
        bar=st.progress(0); stat=st.empty(); err=st.empty()
        def cb(done,total_c): bar.progress(int(done/total_c*100)); stat.markdown(f"⏳ Generating… combo **{done}/{total_c}**")
        try:
            new_qs=generate_batch(st.session_state.api_key,sel_topics,sel_diffs,n_q,existing=existing,progress_cb=cb)
            st.session_state.ai_questions.extend(new_qs); bar.progress(100); stat.empty()
            st.success(f"✅ Generated **{len(new_qs)}** new questions! Total: **{len(QUESTION_BANK)+len(st.session_state.ai_questions)}**")
            st.balloons()
        except anthropic.AuthenticationError: bar.empty(); stat.empty(); err.error("❌ Invalid API key.")
        except anthropic.RateLimitError: bar.empty(); stat.empty(); err.error("❌ Rate limit. Please wait.")
        except Exception as e: bar.empty(); stat.empty(); err.error(f"❌ Error: {str(e)}")
    if st.session_state.ai_questions:
        st.markdown("---"); st.markdown(f"### 📋 AI Questions ({len(st.session_state.ai_questions)} total)")
        pf1,pf2=st.columns(2)
        with pf1: f_t=st.selectbox("Filter topic",["All"]+TOPICS,key="pf_t")
        with pf2: f_d=st.selectbox("Filter difficulty",["All"]+DIFFICULTIES,key="pf_d")
        filtered=st.session_state.ai_questions
        if f_t!="All": filtered=[q for q in filtered if q.get("topic")==f_t]
        if f_d!="All": filtered=[q for q in filtered if q.get("difficulty")==f_d]
        for q in filtered[:15]:
            with st.expander(f"🤖 [{q.get('difficulty','?').upper()}] {q['q'][:85]}..."):
                for opt in q["opts"]:
                    is_a=opt[0]==q["ans"]
                    st.markdown(f"<span style='color:{'#27ae60' if is_a else '#2c2c3e'};font-weight:{'700' if is_a else '400'}'>{'✅ ' if is_a else '   '}{opt}</span>",unsafe_allow_html=True)
        if st.button("🗑️ Clear AI Questions"): st.session_state.ai_questions=[]; st.success("Cleared."); st.rerun()
    st.markdown("---"); st.markdown("### 🔢 Question Count Matrix")
    aq=QUESTION_BANK+st.session_state.ai_questions
    rows=["| Topic | Easy | Medium | Hard | Total |","|---|---|---|---|---|"]
    for t in TOPICS:
        e=len([q for q in aq if q["topic"]==t and q["difficulty"]=="easy"])
        m=len([q for q in aq if q["topic"]==t and q["difficulty"]=="medium"])
        h=len([q for q in aq if q["topic"]==t and q["difficulty"]=="hard"])
        rows.append(f"| {t} | {e} | {m} | {h} | **{e+m+h}** |")
    st.markdown("\n".join(rows))

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
def page_analytics():
    st.markdown("""<div class="app-hdr"><div><h1>📊 Performance Analytics</h1>
    <div class="sub">Track your Kerala SET preparation progress</div></div></div>""",unsafe_allow_html=True)
    att=st.session_state.total_attempted; cor=st.session_state.total_correct
    acc=round(cor/att*100) if att else 0; bst=st.session_state.best_streak
    stat_cards([("Attempted",att,"sc-green"),("Correct",cor,"sc-gold"),
                ("Accuracy",f"{acc}%","sc-blue"),("Best Streak 🔥",bst,"sc-red"),
                ("AI Questions",len(st.session_state.ai_questions),"sc-blue")])
    if att==0:
        st.info("🎯 No data yet — take some quizzes first!")
        if st.button("▶️ Start a Quiz",type="primary"):
            start_quiz(count=10); st.session_state.page="quiz"; st.rerun()
        return
    st.markdown("### 📚 Performance by Topic")
    ts=st.session_state.topic_stats
    for topic in TOPICS:
        s=ts.get(topic,{"attempted":0,"correct":0})
        if s["attempted"]==0: continue
        a=round(s["correct"]/s["attempted"]*100)
        col="#27ae60" if a>=70 else "#e67e22" if a>=50 else "#e74c3c"
        lbl="🟢 Strong" if a>=70 else "🟡 Moderate" if a>=50 else "🔴 Needs Work"
        st.markdown(f"""<div class="tcard">
        <div style="flex:1"><div class="tcard-name">{topic}</div>
        <div class="tcard-sub">{s['correct']}/{s['attempted']} correct</div></div>
        <div><div class="tcard-pct" style="color:{col}">{a}%</div>
        <div class="tcard-lbl" style="color:{col}">{lbl}</div></div></div>
        <div class="pw" style="margin-top:-4px;margin-bottom:6px"><div class="pb" style="width:{a}%;background:{col}"></div></div>""",unsafe_allow_html=True)
    st.markdown("### 🎯 Difficulty Breakdown")
    ds=st.session_state.difficulty_stats
    cols=st.columns(3)
    dc={"easy":"#27ae60","medium":"#2980b9","hard":"#c0392b"}
    for i,diff in enumerate(DIFFICULTIES):
        s=ds.get(diff,{"attempted":0,"correct":0})
        a=round(s["correct"]/s["attempted"]*100) if s["attempted"] else 0
        with cols[i]:
            st.markdown(f"""<div class="dcard" style="border-top:4px solid {dc[diff]}">
            <div class="dcard-pct" style="color:{dc[diff]}">{a}%</div>
            <div class="dcard-name">{diff.capitalize()}</div>
            <div class="dcard-sub">{s['correct']}/{s['attempted']}</div></div>""",unsafe_allow_html=True)
    st.markdown("---"); st.markdown("### 💡 Study Recommendations")
    weak=[t for t in TOPICS if ts.get(t,{}).get("attempted",0)>0 and round(ts[t]["correct"]/ts[t]["attempted"]*100)<60]
    unt=[t for t in TOPICS if ts.get(t,{}).get("attempted",0)==0]
    if weak:
        st.warning(f"**⚠️ Focus Areas:** {', '.join(weak)}")
        if st.button(f"📝 Practice {weak[0]}",type="primary"):
            start_quiz(topic_filter=[weak[0]],count=15); st.session_state.page="quiz"; st.rerun()
    if unt: st.info(f"**📌 Not yet attempted:** {', '.join(unt)}")
    if acc>=75: st.success("🏆 Excellent! Focus on Hard difficulty to sharpen further.")
    elif acc>=55: st.info("📈 Good progress! Practise consistently across all topics.")
    else: st.warning("📖 Keep going! Build confidence with Easy and Medium questions first.")
    st.markdown("---")
    if st.button("🔄 Reset Statistics"):
        for k in ["total_attempted","total_correct","topic_stats","difficulty_stats","best_streak","streak"]:
            st.session_state[k]={} if "stats" in k else 0
        st.success("Statistics reset."); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: QUESTION BANK
# ══════════════════════════════════════════════════════════════════════════════
def page_bank():
    st.markdown("""<div class="app-hdr"><div><h1>📖 Question Bank</h1>
    <div class="sub">Browse, filter and explore all questions</div></div></div>""",unsafe_allow_html=True)
    aq=all_questions(); seed=[q for q in aq if not q.get("ai_generated")]; ai_q=[q for q in aq if q.get("ai_generated")]
    stat_cards([("Total",len(aq),"sc-blue"),("Curated",len(seed),"sc-green"),("AI Generated",len(ai_q),"sc-gold")])
    st.markdown("---")
    col1,col2,col3,col4=st.columns(4)
    with col1: f_t=st.selectbox("Topic",["All"]+TOPICS,key="bk_t")
    with col2: f_d=st.selectbox("Difficulty",["All"]+DIFFICULTIES,key="bk_d")
    with col3: f_s=st.selectbox("Source",["All","Curated","AI"],key="bk_s")
    with col4: srch=st.text_input("Search",placeholder="keyword…",key="bk_q")
    filtered=aq
    if f_t!="All": filtered=[q for q in filtered if q["topic"]==f_t]
    if f_d!="All": filtered=[q for q in filtered if q["difficulty"]==f_d]
    if f_s=="Curated": filtered=[q for q in filtered if not q.get("ai_generated")]
    elif f_s=="AI": filtered=[q for q in filtered if q.get("ai_generated")]
    if srch:
        kw=srch.lower()
        filtered=[q for q in filtered if kw in q["q"].lower() or any(kw in o.lower() for o in q["opts"])]
    PAGE_SIZE=15; total_p=max(1,(len(filtered)+PAGE_SIZE-1)//PAGE_SIZE)
    pg=st.number_input("Page",1,total_p,1,key="bk_pg")
    st.markdown(f"**{len(filtered)}** questions match · Page {pg}/{total_p}")
    for q in filtered[(pg-1)*PAGE_SIZE:pg*PAGE_SIZE]:
        dc=q.get("difficulty","medium"); pre="🤖 " if q.get("ai_generated") else ""
        with st.expander(f"{pre}[{q['topic']} · {dc.upper()}] {q['q'][:90]}{'...' if len(q['q'])>90 else ''}"):
            st.markdown(f"**Topic:** {q['topic']} · **Subtopic:** {q.get('subtopic','')} · **Difficulty:** {dc}")
            for opt in q["opts"]:
                is_a=opt[0]==q["ans"]
                st.markdown(f"<span style='color:{'#27ae60' if is_a else '#2c2c3e'};font-weight:{'700' if is_a else '400'}'>{'✅ ' if is_a else '   '}{opt}</span>",unsafe_allow_html=True)
            if st.button("📝 Practice this topic",key=f"bk_prac_{q['id']}"):
                start_quiz(topic_filter=[q["topic"]],count=10); st.session_state.page="quiz"; st.rerun()
    st.markdown("---")
    if st.button("📥 Export as .txt"):
        lines=[]
        for i,q in enumerate(filtered,1):
            lines.append(f"Q{i}. {q['q']}")
            for opt in q["opts"]: lines.append(f"   {'→ ' if opt[0]==q['ans'] else '  '}{opt}")
            lines.append(f"   Answer: {q['ans']} | {q['topic']} | {q['difficulty']}\n")
        st.download_button("⬇️ Download .txt","\n".join(lines).encode(),"kerala_set_questions.txt","text/plain")

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: IMPORTANT QUOTES
# ══════════════════════════════════════════════════════════════════════════════
def page_quotes():
    st.markdown("""<div class="app-hdr"><div><h1>📜 Important Quotes</h1>
    <div class="sub">Must-know quotations for Kerala SET exam</div></div></div>""",unsafe_allow_html=True)
    search=st.text_input("🔍 Search quotes",placeholder="author, work or keyword…",key="qsearch")
    filtered=IMPORTANT_QUOTES
    if search:
        kw=search.lower()
        filtered=[q for q in filtered if kw in q["quote"].lower() or kw in q["author"].lower() or kw in q["work"].lower()]
    st.markdown(f"**{len(filtered)}** quotes")
    for q in filtered:
        st.markdown(f"""<div class="qquote">
        <blockquote>"{q['quote']}"</blockquote>
        <div class="attr">— <strong>{q['author']}</strong>, <em>{q['work']}</em></div>
        <div style="font-size:.76rem;opacity:.75;margin-top:.4rem;color:#fff">{q['note']}</div></div>""",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: LITERARY TIMELINE
# ══════════════════════════════════════════════════════════════════════════════
def page_timeline():
    st.markdown("""<div class="app-hdr"><div><h1>⏳ Literary Timeline</h1>
    <div class="sub">Key dates in English & World Literature for Kerala SET</div></div></div>""",unsafe_allow_html=True)
    search=st.text_input("🔍 Search timeline",placeholder="author, work or century…",key="tlsearch")
    filtered=TIMELINE_DATA
    if search:
        kw=search.lower()
        filtered=[(yr,ev) for yr,ev in filtered if kw in ev.lower() or kw in yr.lower()]
    st.markdown(f"**{len(filtered)}** events")
    for yr,ev in filtered:
        st.markdown(f"""<div class="tlrow"><div class="tlyr">{yr}</div>
        <div class="tlev">{ev}</div></div>""",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: AUTHOR PROFILES
# ══════════════════════════════════════════════════════════════════════════════
def page_authors():
    st.markdown("""<div class="app-hdr"><div><h1>👤 Author Profiles</h1>
    <div class="sub">Key authors for Kerala SET — biography, works, and exam notes</div></div></div>""",unsafe_allow_html=True)
    search=st.text_input("🔍 Search authors",placeholder="name or period…",key="asearch")
    period_filter=st.selectbox("Filter by period",["All"]+sorted(set(a["period"] for a in AUTHOR_PROFILES)),key="aperiod")
    filtered=AUTHOR_PROFILES
    if search:
        kw=search.lower()
        filtered=[a for a in filtered if kw in a["name"].lower() or kw in a["period"].lower() or kw in a["bio"].lower()]
    if period_filter!="All":
        filtered=[a for a in filtered if a["period"]==period_filter]
    st.markdown(f"**{len(filtered)}** authors")
    for a in filtered:
        with st.expander(f"**{a['name']}** ({a['dates']}) · {a['period']}"):
            st.markdown(f"""<div class="acard">
            <div class="acard-name">{a['name']}</div>
            <div class="acard-dates">{a['dates']} · {a['period']}</div>
            <div class="acard-body">{a['bio']}</div>
            <div class="acard-works">📚 Key works: {a['works']}</div>
            <div style="font-size:.78rem;color:#e65100;margin-top:.4rem;font-weight:500">📌 Exam note: {a['note']}</div></div>""",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: THEORY NOTES
# ══════════════════════════════════════════════════════════════════════════════
def page_theory():
    st.markdown("""<div class="app-hdr"><div><h1>🧠 Literary Theory Notes</h1>
    <div class="sub">Schools of criticism · Key figures · Core concepts · Must-read texts</div></div></div>""",unsafe_allow_html=True)
    selected=st.selectbox("Select theory/school",list(THEORY_NOTES.keys()),key="th_sel")
    t=THEORY_NOTES[selected]
    st.markdown(f"""<div class="ksec"><h4>📌 {selected} — Overview</h4><p>{t['summary']}</p></div>""",unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1:
        st.markdown(f"""<div class="ksec"><h4>👥 Key Figures</h4><p>{t['key_figures']}</p></div>""",unsafe_allow_html=True)
        st.markdown(f"""<div class="ksec"><h4>📖 Key Texts</h4><p>{t['key_texts']}</p></div>""",unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="ksec"><h4>💡 Key Concepts</h4><p>{t['key_concepts']}</p></div>""",unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📋 All Schools at a Glance")
    rows=["| School | Key Figure | Core Concept |","|---|---|---|"]
    glance={"New Criticism":"Cleanth Brooks","Structuralism":"Saussure","Deconstruction":"Derrida",
            "Postcolonialism":"Edward Said","Feminist Criticism":"Elaine Showalter","Marxist Criticism":"Louis Althusser",
            "New Historicism":"Stephen Greenblatt","Psychoanalytic Criticism":"Jacques Lacan"}
    concepts={"New Criticism":"Organic unity, ambiguity","Structuralism":"Signifier/Signified, binary oppositions",
               "Deconstruction":"Différance, logocentrism","Postcolonialism":"Orientalism, hybridity, subaltern",
               "Feminist Criticism":"Gynocriticism, écriture féminine","Marxist Criticism":"Ideology, hegemony, ISA",
               "New Historicism":"Thick description, circulation of energy","Psychoanalytic Criticism":"Mirror stage, the Gaze, uncanny"}
    for school,fig in glance.items():
        rows.append(f"| {school} | {fig} | {concepts.get(school,'')} |")
    st.markdown("\n".join(rows))
    st.markdown("---")
    if st.button("📝 Practice Literary Theory Questions",type="primary"):
        start_quiz(topic_filter=["Literary Theory"],count=15); st.session_state.page="quiz"; st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: LINGUISTICS NOTES
# ══════════════════════════════════════════════════════════════════════════════
def page_linguistics():
    st.markdown("""<div class="app-hdr"><div><h1>📐 Linguistics Notes</h1>
    <div class="sub">Phonetics · Morphology · Semantics · Language Acquisition · Teaching Methods</div></div></div>""",unsafe_allow_html=True)
    selected=st.selectbox("Select topic",list(LINGUISTICS_NOTES.keys()),key="ln_sel")
    n=LINGUISTICS_NOTES[selected]
    st.markdown(f"""<div class="ksec"><h4>📌 {selected} — Overview</h4><p>{n['summary']}</p></div>""",unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1:
        st.markdown(f"""<div class="ksec"><h4>💡 Key Concepts</h4><p>{n['key_concepts']}</p></div>""",unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="ksec"><h4>📝 Examples & Notes</h4><p>{n['examples']}</p></div>""",unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🔡 Quick Reference: Language Teaching Methods")
    methods=[
        ("Grammar-Translation","Oldest method. Translates texts, teaches grammar rules explicitly. Focus on reading/writing. Little spoken communication.","Traditional classrooms"),
        ("Direct Method","No mother tongue allowed. Target language only. Oral-first. Grammar taught inductively.","Alliance Française style"),
        ("Audio-Lingual Method","Behaviourist. Drills and repetition. Pattern practice. Based on Skinner's operant conditioning.","Military language programmes"),
        ("Communicative Language Teaching (CLT)","Function over form. Real-life communication tasks. Fluency over accuracy. Role-plays, discussions.","Most modern EFL classrooms"),
        ("Task-Based Learning (TBL)","Learning through completing meaningful tasks (e.g. plan a trip). Assessment of outcome not just form.","Project-based curricula"),
        ("Natural Approach","Krashen's i+1 input hypothesis. No explicit grammar. Comprehensible input. Silent period respected.","Immersion programmes"),
    ]
    for name,desc,context in methods:
        st.markdown(f"""<div class="ksec"><h4>🔹 {name}</h4>
        <p>{desc}</p><p style="color:#2980b9;font-size:.8rem;margin-top:.3rem">📍 Context: {context}</p></div>""",unsafe_allow_html=True)
    st.markdown("---")
    if st.button("📝 Practice Linguistics Questions",type="primary"):
        start_quiz(topic_filter=["Linguistics"],count=15); st.session_state.page="quiz"; st.rerun()

# ══════════════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════════════
#  FLASHCARD DATA
# ══════════════════════════════════════════════════════════════════════════════
FLASHCARDS = [
    {"front":"Who coined the term 'objective correlative'?","back":"T.S. Eliot","category":"Literary Theory"},
    {"front":"What is Saussure's term for the sound-image in a linguistic sign?","back":"Signifier (as opposed to the Signified, which is the concept)","category":"Linguistics"},
    {"front":"Which novel begins: 'Call me Ishmael'?","back":"Moby-Dick by Herman Melville (1851)","category":"American Literature"},
    {"front":"Who wrote Orientalism (1978)?","back":"Edward Said","category":"Literary Theory"},
    {"front":"What is 'negative capability'?","back":"Keats's phrase for the capacity to remain in uncertainty and doubt without irritably reaching for reason or fact","category":"British Literature"},
    {"front":"What does 'gynocriticism' mean?","back":"Elaine Showalter's term for the study of women as writers — their literary history, styles, themes, genres","category":"Literary Theory"},
    {"front":"Which Modernist novel is set entirely on 16 June 1904?","back":"Ulysses by James Joyce (1922)","category":"British Literature"},
    {"front":"Who wrote 'Can the Subaltern Speak?' (1988)?","back":"Gayatri Chakravorty Spivak","category":"Literary Theory"},
    {"front":"What is 'écriture féminine'?","back":"Hélène Cixous's concept of a female writing practice that disrupts patriarchal discourse through the body","category":"Literary Theory"},
    {"front":"Who is the narrator of Heart of Darkness?","back":"Marlow (Charles Marlow), narrated within a frame story aboard the Thames","category":"British Literature"},
    {"front":"What does 'defamiliarisation' (ostranenie) mean?","back":"Viktor Shklovsky's Russian Formalist concept: making the familiar seem strange to force fresh perception","category":"Literary Theory"},
    {"front":"Which Indian novel won the Booker Prize in 1997?","back":"The God of Small Things by Arundhati Roy","category":"Indian Literature"},
    {"front":"What is Aristotle's term for the moment of recognition in tragedy?","back":"Anagnorisis (as opposed to peripeteia = reversal of fortune)","category":"Literary Theory"},
    {"front":"What are Grice's four conversational maxims?","back":"Quality (be truthful), Quantity (be appropriately informative), Relation (be relevant), Manner (be clear)","category":"Linguistics"},
    {"front":"Who wrote Waiting for Godot and in what year was it first performed?","back":"Samuel Beckett; first performed 5 January 1953 at the Théâtre de Babylone, Paris","category":"British Literature"},
    {"front":"What is the 'intentional fallacy'?","back":"W.K. Wimsatt & Monroe Beardsley's term: the mistake of judging a poem by the author's stated intention","category":"Literary Theory"},
    {"front":"Who coined the term 'intertextuality'?","back":"Julia Kristeva (1967), building on Bakhtin's concept of dialogism","category":"Literary Theory"},
    {"front":"What is the Great Vowel Shift?","back":"A major change in English vowel pronunciation c.1400–1700 that explains why English spelling and pronunciation diverge","category":"Linguistics"},
    {"front":"Name the three Brontë sisters and their pen names.","back":"Charlotte (Currer Bell), Emily (Ellis Bell), Anne (Acton Bell)","category":"British Literature"},
    {"front":"What is Chomsky's 'Language Acquisition Device' (LAD)?","back":"A hypothetical innate mental faculty that enables children to acquire language rapidly and uniformly","category":"Linguistics"},
    {"front":"Who wrote Things Fall Apart and in what year?","back":"Chinua Achebe, 1958","category":"World Literature"},
    {"front":"What does 'peripeteia' mean in Aristotelian drama?","back":"A reversal of fortune — the sudden change in the protagonist's situation, often from good to bad","category":"Literary Theory"},
    {"front":"Who founded the Hogarth Press?","back":"Virginia and Leonard Woolf, in 1917","category":"British Literature"},
    {"front":"What is 'stream of consciousness'?","back":"A narrative technique presenting the continuous flow of a character's thoughts and perceptions; associated with Woolf, Joyce, and Faulkner","category":"British Literature"},
    {"front":"Name two works by Girish Karnad.","back":"Tughlaq (1964), Hayavadana (1971), Nagamandala (1988), Tale Danda (1990)","category":"Indian Literature"},
    {"front":"What is the Harlem Renaissance?","back":"African-American cultural and artistic movement centred in Harlem, New York, c.1920s–1930s; key figures: Langston Hughes, Zora Neale Hurston, Jean Toomer","category":"American Literature"},
    {"front":"What is 'magical realism'?","back":"A literary mode where magical or supernatural elements are presented as matter-of-fact in an otherwise realistic setting; associated with García Márquez, Rushdie, and others","category":"World Literature"},
    {"front":"Who won the Nobel Prize in Literature in 1913?","back":"Rabindranath Tagore (first non-European Nobel laureate in Literature)","category":"Indian Literature"},
    {"front":"What is the difference between 'langue' and 'parole' in Saussure?","back":"Langue = the abstract system of language shared by a community; Parole = the actual individual utterances/speech acts","category":"Linguistics"},
    {"front":"What is Bakhtin's concept of 'heteroglossia'?","back":"The coexistence of multiple voices, social languages, and perspectives within a single text, resisting single authoritative meaning","category":"Literary Theory"},
]

GLOSSARY_TERMS = [
    ("Allegory","A narrative in which characters and events represent abstract ideas or moral qualities (e.g. Bunyan's The Pilgrim's Progress)."),
    ("Alliteration","Repetition of the same consonant sound at the start of nearby words (e.g. 'Peter Piper picked')."),
    ("Ambiguity","The capacity of a text to sustain multiple meanings simultaneously; William Empson identified seven types."),
    ("Anachronism","An error placing something in the wrong historical period, or a deliberate literary device."),
    ("Anagnorisis","Aristotle's term for the moment of recognition or discovery in a drama, often reversing the hero's fortunes."),
    ("Anaphora","Repetition of a word or phrase at the beginning of successive clauses for rhetorical effect."),
    ("Anthropomorphism","Attributing human qualities to animals, gods, or objects."),
    ("Aporia","An irresolvable contradiction or impasse in a text; central to Derridean deconstruction."),
    ("Archetype","A recurring pattern, character, image, or theme that appears across cultures; associated with Jung and Northrop Frye."),
    ("Assonance","The repetition of vowel sounds within nearby words (e.g. 'the rain in Spain stays mainly in the plain')."),
    ("Bathetic","Relating to bathos — an anticlimax created by moving from the elevated to the trivial."),
    ("Bildungsroman","A novel of formation or coming-of-age (e.g. Great Expectations, Jane Eyre, David Copperfield)."),
    ("Blank verse","Unrhymed iambic pentameter; the dominant form of Shakespeare's plays and Milton's Paradise Lost."),
    ("Canon","The body of literary works considered central, authoritative, or worthy of study; contested by postcolonial and feminist critics."),
    ("Catharsis","Aristotle's term for the emotional purgation (pity and fear) experienced by the audience of tragedy."),
    ("Chiasmus","A rhetorical reversal of grammatical structures in successive phrases: 'Ask not what your country can do for you…'"),
    ("Deus ex machina","A contrived resolution introduced artificially at the end of a narrative; literally 'god from the machine'."),
    ("Diegesis","The story world in which characters live and events occur; 'diegetic' sound is heard by characters too."),
    ("Différance","Derrida's neologism combining 'differ' and 'defer'; language creates meaning only through endless deferral."),
    ("Ekphrasis","A literary description of a visual artwork (e.g. Keats's 'Ode on a Grecian Urn')."),
    ("Elegy","A poem of lamentation for the dead (e.g. Milton's Lycidas, Tennyson's In Memoriam)."),
    ("Epiphany","James Joyce's term for a sudden moment of revelation or insight in a character or text."),
    ("Epistolary","Written in the form of letters (e.g. Richardson's Pamela, Clarissa; Shelley's Frankenstein)."),
    ("Focalisation","Narratology term (Genette) for the perspective through which events are perceived; who sees, not who speaks."),
    ("Free indirect discourse","A narrative technique blending third-person narration with a character's thoughts/speech without quotation marks; associated with Austen and Flaubert."),
    ("Hamartia","Aristotle's term for the protagonist's tragic flaw or error of judgement that precipitates their downfall."),
    ("Hegemony","Gramsci's term for the cultural dominance of a ruling class achieved through consent rather than coercion."),
    ("Hyperbole","Deliberate exaggeration for rhetorical or comic effect."),
    ("Intertextuality","Julia Kristeva's term: every text is a mosaic of quotations from and transformations of other texts."),
    ("Irony","A figure of speech where the intended meaning is opposite to the literal meaning; also a structural device in drama."),
    ("Logocentrism","Derrida's term for the Western philosophical tradition that privileges speech over writing and presence over absence."),
    ("Metafiction","Fiction that self-consciously addresses its own fictional status (e.g. Nabokov's Pale Fire, Rushdie's Midnight's Children)."),
    ("Mimesis","Plato's and Aristotle's term for imitation; the representation of reality in art and literature."),
    ("Motif","A recurring element (image, phrase, situation) in a work that contributes to its theme."),
    ("Ode","A formal lyric poem of praise or meditation; major types include Pindaric, Horatian, and Irregular (e.g. Keats's odes)."),
    ("Pastiche","A work that imitates the style of another artist or period, usually affectionately and without satiric intent."),
    ("Pathetic fallacy","Ruskin's term for attributing human emotions to nature (e.g. 'the angry sea')."),
    ("Peripeteia","Aristotle's term for the reversal of fortune in tragedy, typically from prosperity to disaster."),
    ("Polyphony","Bakhtin's term for a narrative containing multiple equally valid voices without a single authoritative authorial voice."),
    ("Postcolonialism","Critical framework examining the cultural, political, and psychological legacies of European colonialism."),
    ("Prolepsis","Anticipation of future events; narrative flashforward; also called anachrony or flash-forward."),
    ("Rhyme royal","A seven-line stanza in iambic pentameter, rhyming ABABBCC; used by Chaucer and Shakespeare."),
    ("Soliloquy","A speech delivered alone on stage, revealing the speaker's inner thoughts; associated with Shakespeare."),
    ("Sonnet","A 14-line lyric poem; major forms: Petrarchan (ABBAABBA CDECDE) and Shakespearean (ABAB CDCD EFEF GG)."),
    ("Subaltern","Spivak's term (from Gramsci): those who are excluded from hegemonic power structures and cannot represent themselves."),
    ("Sublime","The quality of greatness, vastness, or terror that overwhelms and elevates; theorised by Burke and Kant; central to Romantic aesthetics."),
    ("Synecdoche","A figure of speech where a part represents the whole or vice versa (e.g. 'All hands on deck')."),
    ("Terza rima","A three-line stanza scheme rhyming ABA BCB CDC…; used by Dante in the Divine Comedy and Shelley in 'Ode to the West Wind'."),
    ("Unreliable narrator","A narrator whose account is compromised by limited knowledge, self-interest, or delusion (e.g. Stevens in The Remains of the Day)."),
    ("Zeugma","A single verb or adjective governs two or more nouns or clauses, creating a comic or surprising effect."),
]

NOBEL_DATA = [
    (1907,"Rudyard Kipling","UK","Jungle Book, Kim — first English-language winner"),
    (1913,"Rabindranath Tagore","India","First Asian winner; Gitanjali"),
    (1923,"W.B. Yeats","Ireland","'The Second Coming', 'The Lake Isle of Innisfree'"),
    (1925,"George Bernard Shaw","Ireland/UK","Pygmalion, Man and Superman, Heartbreak House"),
    (1930,"Sinclair Lewis","USA","Babbitt, Main Street — first American winner"),
    (1932,"John Galsworthy","UK","The Forsyte Saga"),
    (1948,"T.S. Eliot","UK/USA","The Waste Land, Four Quartets"),
    (1950,"Bertrand Russell","UK","Philosophy and literature"),
    (1953,"Winston Churchill","UK","Awarded for historical writing"),
    (1954,"Ernest Hemingway","USA","The Old Man and the Sea, A Farewell to Arms"),
    (1962,"John Steinbeck","USA","The Grapes of Wrath, Of Mice and Men"),
    (1969,"Samuel Beckett","Ireland","Waiting for Godot, Endgame"),
    (1971,"Pablo Neruda","Chile","Canto General, Twenty Love Poems"),
    (1973,"Patrick White","Australia","Voss, Riders in the Chariot — first Australian winner"),
    (1982,"Gabriel García Márquez","Colombia","One Hundred Years of Solitude"),
    (1986,"Wole Soyinka","Nigeria","Death and the King's Horseman — first African winner"),
    (1991,"Nadine Gordimer","South Africa","Burger's Daughter, July's People"),
    (1992,"Derek Walcott","St Lucia/Caribbean","Omeros, Dream on Monkey Mountain"),
    (1993,"Toni Morrison","USA","Beloved, Song of Solomon, The Bluest Eye"),
    (2001,"V.S. Naipaul","Trinidad/UK","A House for Mr Biswas, In a Free State"),
    (2003,"J.M. Coetzee","South Africa","Disgrace, Waiting for the Barbarians"),
    (2005,"Harold Pinter","UK","The Birthday Party, The Caretaker — playwright"),
    (2006,"Orhan Pamuk","Turkey","My Name Is Red, Snow"),
    (2007,"Doris Lessing","UK","The Golden Notebook"),
    (2013,"Alice Munro","Canada","'Master of the contemporary short story'"),
    (2016,"Bob Dylan","USA","First musician to win; 'Blowin' in the Wind'"),
    (2017,"Kazuo Ishiguro","UK","The Remains of the Day, Never Let Me Go"),
    (2021,"Abdulrazak Gurnah","Tanzania/UK","Paradise, By the Sea — postcolonial fiction"),
    (2022,"Annie Ernaux","France","Autofiction; The Years"),
    (2023,"Jon Fosse","Norway","Septology — notable for Scandinavian drama"),
    (2024,"Han Kang","South Korea","The Vegetarian, Human Acts — first South Korean winner"),
]

PYQ_PATTERNS = {
    "Most Tested Topics": [
        ("British Literature — Modernism","Joyce, Woolf, Eliot — expect 8–12 questions","🔴 Very High"),
        ("Literary Theory","New Criticism, Deconstruction, Feminism, Postcolonialism","🔴 Very High"),
        ("British Literature — Victorian","Dickens, Hardy, Eliot, Tennyson, Arnold","🔴 High"),
        ("British Literature — Romanticism","Wordsworth, Coleridge, Keats, Shelley, Byron","🟠 High"),
        ("Linguistics","Phonetics, Morphology, Semantics, Language Acquisition","🟠 High"),
        ("Indian Literature","Rushdie, Arundhati Roy, Karnad, Tendulkar, Tagore","🟡 Medium-High"),
        ("American Literature","Melville, Dickinson, Hemingway, Faulkner, T.S. Eliot","🟡 Medium"),
        ("World Literature","Achebe, Soyinka, Walcott, Atwood","🟢 Medium"),
        ("British Literature — Renaissance","Shakespeare, Marlowe, Milton, Spenser","🟠 High"),
        ("British Literature — Old English / Medieval","Beowulf, Chaucer","🟡 Medium"),
    ],
    "Recurring Question Types": [
        "Who wrote X? — Identification of author from work title",
        "Which year was X published? — Chronological/date questions",
        "Statement 1 / Statement 2 — True/False pair questions",
        "Match List I with List II — Matching authors to works",
        "Complete the quote — Famous literary quotations",
        "Which period does X belong to? — Literary periodisation",
        "The term X was coined by ___",
        "Which novel/play contains the character X?",
        "What is the subtitle of X?",
        "Which critic wrote X and in which year?",
    ],
    "High-Frequency Authors": [
        ("T.S. Eliot","Waste Land, Prufrock, Four Quartets, objective correlative, dissociation of sensibility"),
        ("Virginia Woolf","Mrs Dalloway, To the Lighthouse, Bloomsbury Group, stream of consciousness"),
        ("James Joyce","Ulysses, Dubliners, Portrait, stream of consciousness, epiphany"),
        ("William Shakespeare","37 plays, 154 sonnets, First Folio 1623, Globe Theatre"),
        ("Geoffrey Chaucer","Canterbury Tales, Troilus and Criseyde, Middle English, Father of English poetry"),
        ("John Milton","Paradise Lost (12 books), Paradise Regained, Samson Agonistes, Areopagitica"),
        ("Edward Said","Orientalism 1978, Culture and Imperialism, postcolonialism"),
        ("Chinua Achebe","Things Fall Apart 1958, Nigerian, response to Conrad"),
        ("Salman Rushdie","Midnight's Children (Booker 1981), Booker of Bookers, magical realism"),
        ("Rabindranath Tagore","Gitanjali, Nobel 1913, first Asian Nobel, translated himself"),
    ]
}


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: FLASHCARDS
# ══════════════════════════════════════════════════════════════════════════════
def page_flashcards():
    st.markdown("""<div class="app-hdr"><div><h1>🃏 Flashcards</h1>
    <div class="sub">Quick-fire revision — click to reveal the answer</div></div></div>""",unsafe_allow_html=True)

    cats = ["All"] + sorted(set(f["category"] for f in FLASHCARDS))
    col1,col2 = st.columns(2)
    with col1: cat_filter = st.selectbox("Category",cats,key="fc_cat")
    with col2: search = st.text_input("Search cards",placeholder="keyword…",key="fc_search")

    filtered = FLASHCARDS
    if cat_filter != "All": filtered = [f for f in filtered if f["category"]==cat_filter]
    if search:
        kw = search.lower()
        filtered = [f for f in filtered if kw in f["front"].lower() or kw in f["back"].lower()]

    st.markdown(f"**{len(filtered)}** flashcards")
    st.markdown("---")

    if "fc_idx" not in st.session_state: st.session_state.fc_idx = 0
    if "fc_revealed" not in st.session_state: st.session_state.fc_revealed = False

    if not filtered:
        st.info("No cards match your filter."); return

    # Clamp index
    idx = st.session_state.fc_idx % len(filtered)
    card = filtered[idx]

    st.markdown(f"""<div class="flash">
    <div class="flash-hint">{card['category']} · Card {idx+1} of {len(filtered)}</div>
    <div class="flash-q">❓ {card['front']}</div>
    {"<div class='flash-a'>✅ " + card['back'] + "</div>" if st.session_state.fc_revealed else "<div class='flash-hint' style='margin-top:.6rem'>👆 Click Reveal to see the answer</div>"}
    </div>""",unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>",unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("👁️ Reveal Answer",use_container_width=True,type="primary"):
            st.session_state.fc_revealed = True; st.rerun()
    with c2:
        if st.button("⬅️ Previous",use_container_width=True):
            st.session_state.fc_idx = (st.session_state.fc_idx - 1) % len(filtered)
            st.session_state.fc_revealed = False; st.rerun()
    with c3:
        if st.button("Next ➡️",use_container_width=True):
            st.session_state.fc_idx = (st.session_state.fc_idx + 1) % len(filtered)
            st.session_state.fc_revealed = False; st.rerun()

    st.markdown("---")
    if st.button("🔀 Random Card",use_container_width=True):
        st.session_state.fc_idx = random.randint(0,len(filtered)-1)
        st.session_state.fc_revealed = False; st.rerun()

    with st.expander("📋 Browse All Cards in This Category"):
        for i,f in enumerate(filtered):
            st.markdown(f"""<div style="background:#f0f4fb;border-radius:8px;padding:10px 14px;margin-bottom:6px">
            <div style="font-weight:600;color:#1a3a6b;font-size:.88rem">Q: {f['front']}</div>
            <div style="font-size:.83rem;color:#2c2c3e;margin-top:4px">A: {f['back']}</div></div>""",unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: GLOSSARY
# ══════════════════════════════════════════════════════════════════════════════
def page_glossary():
    st.markdown("""<div class="app-hdr"><div><h1>📚 Literary Glossary</h1>
    <div class="sub">50+ essential terms for Kerala SET exam</div></div></div>""",unsafe_allow_html=True)

    search = st.text_input("🔍 Search terms",placeholder="e.g. catharsis, bildungsroman…",key="gl_search")
    alpha_filter = st.selectbox("Filter by letter",["All"]+list("ABCDEFGHIJKLMNOPRSTUZ"),key="gl_alpha")

    filtered = GLOSSARY_TERMS
    if search:
        kw = search.lower()
        filtered = [(t,d) for t,d in filtered if kw in t.lower() or kw in d.lower()]
    if alpha_filter != "All":
        filtered = [(t,d) for t,d in filtered if t.upper().startswith(alpha_filter)]

    st.markdown(f"**{len(filtered)}** terms")
    st.markdown("---")

    for term,defn in filtered:
        st.markdown(f"""<div class="gterm">
        <div class="gterm-word">{term}</div>
        <div class="gterm-def">{defn}</div></div>""",unsafe_allow_html=True)

    st.markdown("---")
    if st.button("📝 Quiz on Literary Theory",type="primary"):
        start_quiz(topic_filter=["Literary Theory"],count=15)
        st.session_state.page="quiz"; st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: NOBEL PRIZE TRACKER
# ══════════════════════════════════════════════════════════════════════════════
def page_nobel():
    st.markdown("""<div class="app-hdr"><div><h1>🏆 Nobel Prize in Literature</h1>
    <div class="sub">Winners frequently tested in Kerala SET — countries, works, and exam notes</div></div></div>""",unsafe_allow_html=True)

    region_filter = st.selectbox("Filter by region",
        ["All","UK","Ireland","USA","India","Nigeria","South Africa","Caribbean","Canada","Other"],key="nb_region")
    search = st.text_input("🔍 Search",placeholder="author or work…",key="nb_search")

    def region_match(country, region):
        if region == "All": return True
        region_map = {"UK":["UK"],"Ireland":["Ireland"],"USA":["USA"],
                      "India":["India"],"Nigeria":["Nigeria"],"South Africa":["South Africa"],
                      "Caribbean":["St Lucia/Caribbean","Trinidad/UK"],
                      "Canada":["Canada"],"Other":[]}
        if region == "Other":
            known = [c for lst in region_map.values() for c in lst if lst]
            return country not in known
        return country in region_map.get(region,[region])

    filtered = [(yr,name,country,note) for yr,name,country,note in NOBEL_DATA
                if region_match(country,region_filter)]
    if search:
        kw = search.lower()
        filtered = [(yr,n,c,nt) for yr,n,c,nt in filtered if kw in n.lower() or kw in nt.lower() or kw in c.lower()]

    filtered = sorted(filtered,key=lambda x:x[0],reverse=True)
    st.markdown(f"**{len(filtered)}** laureates")
    st.markdown("---")

    for yr,name,country,note in filtered:
        st.markdown(f"""<div style="background:#ffffff;border-radius:10px;padding:12px 16px;
        margin-bottom:7px;box-shadow:0 2px 8px rgba(0,0,0,.07);
        display:flex;align-items:center;gap:14px;border-left:4px solid #d4a017">
        <div style="font-size:1.3rem;font-weight:800;color:#8a6200;min-width:55px">{yr}</div>
        <div style="flex:1">
          <div style="font-weight:700;font-size:.95rem;color:#1c1c2e">{name}</div>
          <div style="font-size:.78rem;color:#5a6a7d;margin-top:1px">🌍 {country}</div>
          <div style="font-size:.82rem;color:#2c2c3e;margin-top:3px">{note}</div>
        </div></div>""",unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📌 Exam Tips for Nobel Questions")
    tips = [
        ("First Nobel in Literature","Sully Prudhomme (France, 1901) — not tested often"),
        ("First Asian winner","Rabindranath Tagore (India, 1913) — very frequently tested"),
        ("First African winner","Wole Soyinka (Nigeria, 1986)"),
        ("First American winner","Sinclair Lewis (USA, 1930)"),
        ("First Australian winner","Patrick White (1973)"),
        ("First South Korean winner","Han Kang (2024)"),
        ("Only Indian winner","Rabindranath Tagore (1913)"),
        ("Playwright winners","G.B. Shaw (1925), Beckett (1969), Pinter (2005)"),
        ("Musician winner","Bob Dylan (2016) — frequently asked as a surprise fact"),
        ("Youngest winner","Rudyard Kipling (1907) at age 41"),
    ]
    for label,tip in tips:
        st.markdown(f"""<div style="background:#f8faff;border-radius:8px;padding:9px 14px;
        margin-bottom:5px;border-left:3px solid #2980b9">
        <span style="font-weight:700;color:#1a3a6b">{label}: </span>
        <span style="color:#2c2c3e;font-size:.88rem">{tip}</span></div>""",unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: PYQ ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
def page_pyq():
    st.markdown("""<div class="app-hdr"><div><h1>📋 PYQ Pattern Analysis</h1>
    <div class="sub">Previous Year Question trends · Focus areas · High-frequency authors</div></div></div>""",unsafe_allow_html=True)

    tab1,tab2,tab3 = st.tabs(["🎯 Most Tested Topics","🔄 Question Types","✍️ High-Frequency Authors"])

    with tab1:
        st.markdown("### Most Tested Topics (Based on PYQ Pattern Analysis)")
        st.info("Kerala SET typically has **120 questions** in **120 minutes**. Distribution below is approximate.")
        for topic,detail,freq in PYQ_PATTERNS["Most Tested Topics"]:
            col="#c0392b" if "Very High" in freq else "#e67e22" if "High" in freq else "#f39c12" if "Medium-High" in freq else "#27ae60"
            st.markdown(f"""<div style="background:#ffffff;border-radius:10px;padding:12px 16px;
            margin-bottom:6px;box-shadow:0 2px 8px rgba(0,0,0,.07);
            display:flex;align-items:flex-start;gap:12px;border-left:4px solid {col}">
            <div style="flex:1">
              <div style="font-weight:700;font-size:.93rem;color:#1c1c2e">{topic}</div>
              <div style="font-size:.8rem;color:#5a6a7d;margin-top:3px">{detail}</div>
            </div>
            <div style="font-size:.8rem;font-weight:700;color:{col};white-space:nowrap">{freq}</div>
            </div>""",unsafe_allow_html=True)

    with tab2:
        st.markdown("### Recurring Question Types in Kerala SET PYQs")
        st.markdown("Understanding the format is as important as knowing the content.")
        for i,qt in enumerate(PYQ_PATTERNS["Recurring Question Types"],1):
            st.markdown(f"""<div style="background:#f0f4fb;border-radius:8px;padding:9px 14px;
            margin-bottom:5px;border-left:3px solid #1a3a6b">
            <span style="font-weight:700;color:#1a3a6b;margin-right:8px">{i}.</span>
            <span style="color:#2c2c3e;font-size:.88rem">{qt}</span></div>""",unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### 📌 Strategic Preparation Tips")
        strategies = [
            ("Know full names","Always learn the complete name: e.g. 'Gayatri Chakravorty Spivak', 'Elaine Showalter'"),
            ("Learn dates","Publication year questions are very common: Orientalism (1978), Ulysses (1922)"),
            ("Know subtitles","e.g. Vanity Fair: 'A Novel without a Hero'; Middlemarch: 'A Study of Provincial Life'"),
            ("Pen names","Charlotte Brontë = Currer Bell; George Eliot = Mary Ann Evans; Saki = H.H. Munro"),
            ("First/last works","Frequently asked: e.g. Orwell's last novel (1984), Woolf's last novel (Between the Acts)"),
            ("National firsts","Who was the first X? Very common pattern in SET exams"),
            ("Pairs of works","E.g. Lyrical Ballads (Wordsworth AND Coleridge); First Folio (Shakespeare, published posthumously by friends)"),
        ]
        for tip,detail in strategies:
            st.markdown(f"""<div style="background:#fff8e1;border-radius:8px;padding:9px 14px;
            margin-bottom:5px;border-left:3px solid #f39c12">
            <div style="font-weight:700;color:#8a6200;font-size:.88rem">{tip}</div>
            <div style="font-size:.83rem;color:#2c2c3e;margin-top:2px">{detail}</div></div>""",unsafe_allow_html=True)

    with tab3:
        st.markdown("### High-Frequency Authors — What to Know")
        for author,notes in PYQ_PATTERNS["High-Frequency Authors"]:
            with st.expander(f"✍️ {author}"):
                st.markdown(f"""<div style="background:#f0f4fb;border-radius:8px;padding:12px 14px">
                <div style="font-weight:700;color:#1a3a6b;margin-bottom:6px">{author}</div>
                <div style="font-size:.86rem;color:#2c2c3e;line-height:1.6">{notes}</div></div>""",unsafe_allow_html=True)
                if st.button(f"📝 Practice {author.split()[0]} questions",key=f"pyq_prac_{author}"):
                    kw = author.split()[0].lower()
                    matching = [q for q in all_questions() if kw in q["q"].lower() or any(kw in o.lower() for o in q["opts"])]
                    if matching:
                        random.shuffle(matching)
                        st.session_state.quiz_questions=matching[:10]
                        st.session_state.current_idx=0; st.session_state.answers={}
                        st.session_state.quiz_started=True; st.session_state.quiz_finished=False
                        st.session_state.score=0; st.session_state.streak=0
                        st.session_state.page="quiz"; st.rerun()
                    else:
                        st.info("No questions found for this author — try AI Generation!")

#  ROUTER
# ══════════════════════════════════════════════════════════════════════════════
page=st.session_state.page
if   page=="home":        page_home()
elif page=="quiz":        page_quiz()
elif page=="ai_gen":      page_ai_gen()
elif page=="analytics":   page_analytics()
elif page=="bank":        page_bank()
elif page=="quotes":      page_quotes()
elif page=="timeline":    page_timeline()
elif page=="authors":     page_authors()
elif page=="theory":      page_theory()
elif page=="linguistics": page_linguistics()
elif page=="flashcards": page_flashcards()
elif page=="glossary":    page_glossary()
elif page=="nobel":       page_nobel()
elif page=="pyq":         page_pyq()
else:                     page_home()
