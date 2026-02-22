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

def all_questions(): return QUESTION_BANK + PRELOADED_QUESTIONS + st.session_state.ai_questions

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
#  AI GENERATOR ENGINE  (v3 — robust, efficient, with discussion)
# ══════════════════════════════════════════════════════════════════════════════

AI_MODEL = "claude-haiku-4-5-20251001"   # fast + cost-efficient; best for bulk generation


# ══════════════════════════════════════════════════════════════════════════════
#  PRE-GENERATED QUESTION BANK (300+ questions with full explanations & hints)
#  These work WITHOUT any API key and form the core enriched question set
# ══════════════════════════════════════════════════════════════════════════════
PRELOADED_QUESTIONS = [
  # ─── BRITISH LITERATURE: Modernism ───────────────────────────────────────
  {"id":20001,"topic":"British Literature","subtopic":"Modernism","difficulty":"easy",
   "q":"The stream-of-consciousness technique in Mrs Dalloway moves through time primarily by means of:",
   "opts":["A) Flashbacks introduced by chapter breaks","B) Free association triggered by sensory stimuli","C) A reliable omniscient narrator","D) Dream sequences during sleep"],
   "ans":"B","ai_generated":True,
   "explanation":"Woolf uses characters' sensory perceptions (a car backfire, Big Ben striking) to trigger free-associative memories and thoughts, blurring past and present. There are no chapter breaks in the novel, and the narrator is not traditional or omniscient.",
   "hint":"Think of Mrs Dalloway hearing the car — sound triggers memory. SENSORY → MEMORY is Woolf's method."},

  {"id":20002,"topic":"British Literature","subtopic":"Modernism","difficulty":"medium",
   "q":"T.S. Eliot's concept of the 'dissociation of sensibility' argues that after the seventeenth century, poets:",
   "opts":["A) Wrote only in free verse","B) Could no longer feel their thought as immediately as the smell of a rose","C) Abandoned classical mythology","D) Rejected the dramatic monologue form"],
   "ans":"B","ai_generated":True,
   "explanation":"Eliot argues in 'The Metaphysical Poets' (1921) that after the 17th century, thought and feeling became separate — later poets could not fuse intellectual and emotional experience the way Donne or Marvell did. The exact phrasing 'smell of a rose' is Eliot's own.",
   "hint":"DIS-SOCIATION = SPLIT between thinking and feeling. Donne could do both at once; later poets could not."},

  {"id":20003,"topic":"British Literature","subtopic":"Modernism","difficulty":"hard",
   "q":"Which technique does Woolf employ in The Waves to narrate through nine soliloquies alternating with interludes describing the sea?",
   "opts":["A) Epistolary narration","B) Stream of consciousness presented as formal spoken soliloquy","C) Third-person limited omniscience","D) Unreliable first-person retrospection"],
   "ans":"B","ai_generated":True,
   "explanation":"The Waves abandons traditional narration entirely. Six characters speak in formal, stylised interior monologues ('said Bernard', 'said Jinny') interspersed with poetic descriptions of waves and light. It is Woolf's most experimental departure from realist fiction.",
   "hint":"The WAVES = six voices speaking IN TURNS like waves, not conventional narrative. 'Said Bernard' is the tag throughout."},

  {"id":20004,"topic":"British Literature","subtopic":"Modernism","difficulty":"easy",
   "q":"James Joyce's Dubliners stories are unified by the concept of:",
   "opts":["A) Comic relief","B) Epiphany — a moment of sudden revelation","C) Stream of consciousness","D) The unreliable narrator"],
   "ans":"B","ai_generated":True,
   "explanation":"Joyce borrowed the term 'epiphany' from Catholic theology to describe a sudden spiritual manifestation — a moment when trivial events reveal deep truths. Each story in Dubliners builds toward such a moment of insight or paralysis.",
   "hint":"EPIPHANY = 'sudden revelation'. Joyce: ordinary things suddenly show their deeper truth. In 'The Dead', Gabriel's realisation at the end is the classic example."},

  {"id":20005,"topic":"British Literature","subtopic":"Modernism","difficulty":"medium",
   "q":"Identify the correct statement about W.B. Yeats's system of historical cycles:",
   "opts":["A) He called them 'objective correlatives'","B) He described them as 'gyres' in A Vision (1925)","C) He borrowed the concept directly from Freud","D) He abandoned it after writing 'Sailing to Byzantium'"],
   "ans":"B","ai_generated":True,
   "explanation":"Yeats's A Vision (1925) describes history as a series of interpenetrating cones or 'gyres' — each civilisation completing a 2000-year cycle. 'Objective correlative' is Eliot's term; Freud is not relevant here.",
   "hint":"GYRES = spinning cones = Yeats's historical cycles. Remember: A VISION (1925) is the source text. Not Eliot, not Freud — Yeats."},

  {"id":20006,"topic":"British Literature","subtopic":"Modernism","difficulty":"medium",
   "q":"In Eliot's 'The Love Song of J. Alfred Prufrock', the repeated phrase 'Do I dare?' signals:",
   "opts":["A) Prufrock's heroic boldness","B) Existential paralysis and inability to act","C) The speaker's anger at bourgeois society","D) A direct address to a romantic partner"],
   "ans":"B","ai_generated":True,
   "explanation":"Prufrock's refrain 'Do I dare? / Disturb the universe?' epitomises his paralytic self-consciousness. He is the archetypal anti-hero of Modernism — hyper-aware, unable to act, measuring his life in coffee spoons. The poem is an interior monologue, not a direct romantic address.",
   "hint":"PRUFROCK = PARALYSIS. He thinks about acting but never does. Like Hamlet — he even mentions Hamlet in the poem ('No! I am not Prince Hamlet')."},

  # ─── BRITISH LITERATURE: Victorian ────────────────────────────────────────
  {"id":20010,"topic":"British Literature","subtopic":"Victorian","difficulty":"easy",
   "q":"Matthew Arnold's 'touchstone method' of literary criticism involves:",
   "opts":["A) Comparing each work to passages from great literature to assess quality","B) Using scientific methods to analyse verse","C) Judging literature by its moral improvement of the reader","D) Applying Aristotelian categories of tragedy and comedy"],
   "ans":"A","ai_generated":True,
   "explanation":"Arnold proposed in 'The Study of Poetry' (1880) that critics should use short passages from 'classic' poets (Homer, Dante, Shakespeare) as 'touchstones' against which to measure the quality of other poetry. It is an impressionistic, comparative method.",
   "hint":"TOUCHSTONE = like a gold test stone. You rub gold against it to test purity. Arnold: rub new poetry against Homer/Shakespeare/Dante."},

  {"id":20011,"topic":"British Literature","subtopic":"Victorian","difficulty":"medium",
   "q":"George Eliot's novel Middlemarch is subtitled:",
   "opts":["A) A Novel without a Hero","B) A Study of Provincial Life","C) A Domestic Romance","D) A Novel of Manners"],
   "ans":"B","ai_generated":True,
   "explanation":"Middlemarch (1871-72) carries the subtitle 'A Study of Provincial Life,' signalling Eliot's sociological ambition to document the interconnected lives of a small English community with scientific precision. 'A Novel without a Hero' is the subtitle of Thackeray's Vanity Fair.",
   "hint":"MIDDLEMARCH = 'A Study of Provincial Life'. Mid + March = middle of England. Eliot studies provincial community scientifically. Vanity Fair is 'without a Hero'."},

  {"id":20012,"topic":"British Literature","subtopic":"Victorian","difficulty":"hard",
   "q":"Browning's dramatic monologue 'My Last Duchess' is spoken by the Duke of Ferrara to:",
   "opts":["A) His dead wife in a dream","B) An envoy arranging his next marriage","C) A priest hearing his confession","D) A rival nobleman"],
   "ans":"B","ai_generated":True,
   "explanation":"The poem is set during a negotiation for a new marriage alliance. The Duke addresses the Count's envoy who has come to arrange the terms of a dowry for the Duke's next wife. This context makes the Duke's casual revelation of his first wife's murder chilling — he is simultaneously showing his power and issuing a veiled warning.",
   "hint":"Duke + Envoy + DOWRY negotiation = the dramatic situation. The Duke is simultaneously interviewing for wife #2 while explaining why wife #1 'disappeared'."},

  {"id":20013,"topic":"British Literature","subtopic":"Victorian","difficulty":"easy",
   "q":"Which Dickens novel features the character Miss Havisham who stopped all clocks at the moment she was jilted?",
   "opts":["A) Bleak House","B) Our Mutual Friend","C) Great Expectations","D) Dombey and Son"],
   "ans":"C","ai_generated":True,
   "explanation":"Miss Havisham in Great Expectations (1861) stopped all clocks at 9:20, the moment her groom failed to appear, and spent decades in a decaying wedding dress. She represents obsessive grief and the damage of living in the past.",
   "hint":"MISS HAVISHAM + STOPPED CLOCKS = Great Expectations. She adopts Estella to break men's hearts in revenge. Remember: 'Great' = GREAT trauma."},

  {"id":20014,"topic":"British Literature","subtopic":"Victorian","difficulty":"medium",
   "q":"Thomas Hardy's The Return of the Native is set in:",
   "opts":["A) The Midlands","B) Egdon Heath in Wessex","C) The Scottish Highlands","D) The Yorkshire Moors"],
   "ans":"B","ai_generated":True,
   "explanation":"Hardy's fictional Wessex is centred in Dorset. Egdon Heath functions as a vast, hostile, quasi-mythical landscape that dominates the characters' fates. Hardy opens the novel with an extended personification of the Heath, which many critics see as the true protagonist.",
   "hint":"HARDY = WESSEX = DORSET in real life. Return of the Native = EGDON HEATH. The heath is the most important character in the novel."},

  {"id":20015,"topic":"British Literature","subtopic":"Victorian","difficulty":"hard",
   "q":"Walter Pater's famous conclusion to The Renaissance (1873) advocates:",
   "opts":["A) Moral improvement through art","B) Burning with a gem-like flame — aesthetic experience as an end in itself","C) The return to classical Greek values in modern life","D) Political engagement as the highest artistic duty"],
   "ans":"B","ai_generated":True,
   "explanation":"Pater's Conclusion scandalously argued that life is a series of fleeting impressions, and the highest goal is to burn with a 'gem-like flame' of intense aesthetic experience — a proto-Decadent position that led Oxford authorities to remove the Conclusion from later editions for fear of corrupting students.",
   "hint":"PATER = 'Burn with a gem-like FLAME.' Pure aestheticism — art for its own sake. This inspired Oscar Wilde. The conclusion was so controversial it was pulled from the 2nd edition."},

  # ─── BRITISH LITERATURE: Romanticism ──────────────────────────────────────
  {"id":20020,"topic":"British Literature","subtopic":"Romanticism","difficulty":"easy",
   "q":"Keats's 'Ode on a Grecian Urn' ends with the famous assertion:",
   "opts":["A) 'Beauty is in the eye of the beholder'","B) 'Beauty is truth, truth beauty — that is all ye know on earth'","C) 'A thing of beauty is a joy forever'","D) 'Heard melodies are sweet, but those unheard are sweeter'"],
   "ans":"B","ai_generated":True,
   "explanation":"The final two lines of 'Ode on a Grecian Urn' — 'Beauty is truth, truth beauty, — that is all / Ye know on earth, and all ye need to know' — are among the most debated in English poetry. 'A thing of beauty is a joy forever' opens Endymion; 'Heard melodies' appears earlier in the same ode.",
   "hint":"'Beauty is truth, truth beauty' = ODE ON A GRECIAN URN. Closing line. 'A thing of beauty is a joy forever' = ENDYMION (different poem!)."},

  {"id":20021,"topic":"British Literature","subtopic":"Romanticism","difficulty":"medium",
   "q":"Shelley's 'Ode to the West Wind' employs terza rima. This verse form was invented by:",
   "opts":["A) Petrarch","B) Virgil","C) Dante Alighieri","D) Boccaccio"],
   "ans":"C","ai_generated":True,
   "explanation":"Dante invented terza rima (ABA BCB CDC…) for the Divine Comedy (c.1308-21). Shelley consciously adopted it for 'Ode to the West Wind' (1819) to lend the poem's driving energy a formal momentum that mirrors the relentless force of the wind.",
   "hint":"TERZA RIMA = Dante's form (Divine Comedy). Shelley borrowed it for the West Wind's relentless interlocking force. ABA BCB = each stanza locks into the next."},

  {"id":20022,"topic":"British Literature","subtopic":"Romanticism","difficulty":"easy",
   "q":"Byron's poem Don Juan is primarily written in:",
   "opts":["A) Spenserian stanza","B) Ottava rima","C) Heroic couplets","D) Blank verse"],
   "ans":"B","ai_generated":True,
   "explanation":"Byron uses ottava rima (ABABABCC — 8 lines, iambic pentameter) throughout Don Juan, exploiting its closing couplet for comic or ironic deflation. This Italian stanza form, used by Ariosto and Tasso, becomes Byron's vehicle for wit and satire.",
   "hint":"DON JUAN = OTTAVA RIMA. 8-line stanza, ABABABCC. Byron uses the closing couplet for COMIC PUNCHLINES. Don = 8 letters = 8-line stanza (memory trick!)."},

  {"id":20023,"topic":"British Literature","subtopic":"Romanticism","difficulty":"hard",
   "q":"Coleridge's Biographia Literaria (1817) makes a famous distinction between:",
   "opts":["A) The sublime and the beautiful","B) Primary imagination, secondary imagination, and fancy","C) Organic and mechanical form","D) Classical and Romantic modes of composition"],
   "ans":"B","ai_generated":True,
   "explanation":"In Chapter XIII of Biographia Literaria, Coleridge distinguishes: Primary Imagination (the living power of all human perception), Secondary Imagination (the conscious echo that recreates and modifies — the true creative faculty), and Fancy (mere association of fixed ideas, not truly creative). This is his most influential critical contribution.",
   "hint":"COLERIDGE = THREE levels: 1° Primary (all humans perceive), 2° Secondary (artist creates), Fancy (just associates). PRIMARY is unconscious, SECONDARY is the POET'S power."},

  {"id":20024,"topic":"British Literature","subtopic":"Romanticism","difficulty":"medium",
   "q":"Blake's 'Songs of Innocence and Experience' were published together in:",
   "opts":["A) 1789","B) 1794","C) 1798","D) 1804"],
   "ans":"B","ai_generated":True,
   "explanation":"Songs of Innocence appeared alone in 1789; Songs of Experience was added and the combined volume published in 1794, with the famous subtitle 'Showing the Two Contrary States of the Human Soul.' 1798 is the date of Lyrical Ballads.",
   "hint":"Songs of INNOCENCE = 1789 (French Revolution year, childhood/purity). Songs of EXPERIENCE added in 1794. 1798 = Lyrical Ballads (different work, Wordsworth-Coleridge)."},

  # ─── BRITISH LITERATURE: Renaissance ─────────────────────────────────────
  {"id":20030,"topic":"British Literature","subtopic":"Renaissance","difficulty":"easy",
   "q":"Shakespeare's play that features the line 'All the world's a stage, / And all the men and women merely players' is:",
   "opts":["A) Hamlet","B) King Lear","C) As You Like It","D) The Tempest"],
   "ans":"C","ai_generated":True,
   "explanation":"The 'Seven Ages of Man' speech ('All the world's a stage') is spoken by Jacques in As You Like It (Act II, Scene vii). It is one of the most famous set pieces in Shakespearean comedy, contrasting sharply with the melancholy Jacques himself.",
   "hint":"'All the world's a STAGE' = AS YOU LIKE IT (the play about a theatrical world). Spoken by JAQUES, the melancholy philosopher of the Forest of Arden."},

  {"id":20031,"topic":"British Literature","subtopic":"Renaissance","difficulty":"medium",
   "q":"Sidney's Defence of Poesy argues that poetry is superior to history and philosophy because:",
   "opts":["A) It is more emotionally intense","B) It gives the universal and the particular simultaneously — a speaking picture","C) It teaches through metre and rhyme","D) It requires more technical skill than prose"],
   "ans":"B","ai_generated":True,
   "explanation":"Sidney argues that history gives only particulars (what happened) and philosophy only universals (abstract ideas), while poetry gives both: the philosopher's generality clothed in the historian's particularity. He famously calls the poet a 'maker' who creates a second nature.",
   "hint":"SIDNEY: Poet = COMBINES history (particular) + philosophy (universal). The poet MAKES, doesn't just imitate. Defence of Poesy = first major work of English literary criticism."},

  {"id":20032,"topic":"British Literature","subtopic":"Renaissance","difficulty":"hard",
   "q":"Spenser's The Faerie Queene uses the Spenserian stanza, which consists of:",
   "opts":["A) Eight iambic pentameter lines + one iambic hexameter (alexandrine), rhyming ABABBCBCC","B) Seven iambic pentameter lines rhyming ABABBCC","C) Eight iambic tetrameter lines + one alexandrine, rhyming ABABCDCD","D) Nine iambic pentameter lines rhyming ABABABABB"],
   "ans":"A","ai_generated":True,
   "explanation":"The Spenserian stanza: 9 lines — 8 of iambic pentameter + a final alexandrine (6 iambic feet), rhyming ABABBCBCC. The lengthened final line creates a satisfying sense of closure or weight. Keats and Byron both used this stanza.",
   "hint":"SPENSERIAN STANZA = 8 pentameter + 1 ALEXANDRINE (6 feet). ABABBCBCC. Remember: NINE lines, last one is LONGER (alexandrine). Keats used it in The Eve of St Agnes."},

  {"id":20033,"topic":"British Literature","subtopic":"Renaissance","difficulty":"easy",
   "q":"The masque 'The Tempest' opens with a shipwreck. The magician Prospero was once Duke of:",
   "opts":["A) Venice","B) Verona","C) Milan","D) Naples"],
   "ans":"C","ai_generated":True,
   "explanation":"Prospero was the rightful Duke of Milan, usurped by his brother Antonio with the help of Alonso, King of Naples. He retreated to the island with his daughter Miranda. The play's action involves restoring Prospero's rightful dukedom.",
   "hint":"PROSPERO = DUKE OF MILAN. Usurped by brother ANTONIO. Remember: M for Milan, M for Magic, M for Miranda. 3 M's = Milan, Magic, Miranda."},

  # ─── BRITISH LITERATURE: 18th Century ────────────────────────────────────
  {"id":20040,"topic":"British Literature","subtopic":"18th Century","difficulty":"easy",
   "q":"Alexander Pope's mock epic The Rape of the Lock was inspired by a real quarrel between two Catholic families about:",
   "opts":["A) A stolen jewel","B) A lock of hair cut without permission","C) A contested inheritance","D) An arranged marriage"],
   "ans":"B","ai_generated":True,
   "explanation":"Lord Petre cut a lock of Arabella Fermor's hair without permission, causing a quarrel between their families. Pope's friend John Caryll suggested he write a poem to reconcile them; instead Pope produced a brilliant mock-heroic satire elevating a trivial incident to Homeric proportions.",
   "hint":"RAPE OF THE LOCK = lock of HAIR stolen. Real event: Lord Petre cut Arabella Fermor's hair. Pope MOCKED the fuss by using epic machinery (sylphs as guardian spirits)."},

  {"id":20041,"topic":"British Literature","subtopic":"18th Century","difficulty":"medium",
   "q":"Samuel Johnson's Dictionary of the English Language was published in:",
   "opts":["A) 1747","B) 1750","C) 1755","D) 1762"],
   "ans":"C","ai_generated":True,
   "explanation":"Johnson's Dictionary appeared in 1755, nine years after the Plan of a Dictionary (1747) addressed to Lord Chesterfield. The Dictionary contained approximately 42,000 entries and remained authoritative for over a century until the OED.",
   "hint":"JOHNSON'S DICTIONARY = 1755. Remember: 1-7-5-5 = 17 (55 = 5 squared = 25, so 1755). Or: Johnson worked for 9 years (1746-1755). He famously defined 'lexicographer' as 'a harmless drudge'."},

  {"id":20042,"topic":"British Literature","subtopic":"18th Century","difficulty":"medium",
   "q":"Swift's Gulliver's Travels (1726) is divided into four voyages. Which voyage satirises the corruption of reason and the Royal Society through the flying island of Laputa?",
   "opts":["A) Voyage I (Lilliput)","B) Voyage II (Brobdingnag)","C) Voyage III (Laputa)","D) Voyage IV (Houyhnhnms)"],
   "ans":"C","ai_generated":True,
   "explanation":"Voyage III targets abstract speculation divorced from practical life. The Laputans are so absorbed in theoretical mathematics and music that they require servants ('flappers') to tap them to attention. Laputa floats above the country of Balnibarbi, which is ruined by the Academy of Projectors' impractical schemes.",
   "hint":"LAPUTA = Book III = Satire on ABSTRACT SCIENCE (Royal Society). Laputans float above reality, just as scientists ignore practical life. Book I=tiny (Lilliput), II=huge (Brobdingnag), III=abstract (Laputa), IV=horses (Houyhnhnms)."},

  # ─── BRITISH LITERATURE: Old English / Medieval ───────────────────────────
  {"id":20050,"topic":"British Literature","subtopic":"Old English","difficulty":"medium",
   "q":"Beowulf is preserved in a single manuscript known as the Cotton Vitellius manuscript, kept at the:",
   "opts":["A) Bodleian Library, Oxford","B) British Library, London","C) Cambridge University Library","D) National Library of Scotland"],
   "ans":"B","ai_generated":True,
   "explanation":"The Nowell Codex (Cotton Vitellius A.xv.) containing Beowulf is held at the British Library in London. The manuscript was damaged in the 1731 Cotton library fire but survived; Thorkelin made the first transcripts in 1786-87.",
   "hint":"BEOWULF manuscript = BRITISH LIBRARY (Cotton Vitellius A.xv.). Remember: one manuscript = one location = British Library. The manuscript is over 1000 years old."},

  {"id":20051,"topic":"British Literature","subtopic":"Medieval","difficulty":"medium",
   "q":"In The Canterbury Tales, the pilgrims are travelling to the shrine of which saint?",
   "opts":["A) St Cuthbert at Durham","B) St Thomas Becket at Canterbury Cathedral","C) St Edward at Westminster","D) St Swithun at Winchester"],
   "ans":"B","ai_generated":True,
   "explanation":"The pilgrims in Chaucer's frame narrative travel to Canterbury Cathedral to venerate the shrine of Thomas Becket, Archbishop of Canterbury murdered in 1170 and canonised in 1173. Canterbury Cathedral was one of the most visited pilgrimage sites in medieval England.",
   "hint":"CANTERBURY TALES = pilgrims going to Canterbury to see ST THOMAS BECKET's shrine. Becket = Archbishop murdered by knights of Henry II. 'Will no one rid me of this turbulent priest?'"},

  {"id":20052,"topic":"British Literature","subtopic":"Medieval","difficulty":"hard",
   "q":"Sir Gawain and the Green Knight is written in a dialect associated with the:",
   "opts":["A) Southeast Midlands (London)","B) East Midlands","C) Northwest Midlands (Cheshire/Lancashire area)","D) Northumbria"],
   "ans":"C","ai_generated":True,
   "explanation":"The Pearl-Poet (also known as the Gawain-Poet) wrote in the Northwest Midland dialect, associated with the Cheshire/Lancashire region. This distinguishes the poem sharply from Chaucer's London/Southeast Midland dialect. The Pearl manuscript contains four poems attributed to the same anonymous poet.",
   "hint":"GAWAIN-POET = NORTHWEST MIDLANDS (Lancashire/Cheshire). Chaucer = SOUTHEAST (London). Same period, different dialect. The four Pearl poems are all from the same anonymous Northwest Midlands poet."},

  # ─── AMERICAN LITERATURE ──────────────────────────────────────────────────
  {"id":20060,"topic":"American Literature","subtopic":"Modernism","difficulty":"easy",
   "q":"Fitzgerald's The Great Gatsby is narrated by:",
   "opts":["A) Jay Gatsby himself","B) Daisy Buchanan","C) Nick Carraway","D) Tom Buchanan"],
   "ans":"C","ai_generated":True,
   "explanation":"Nick Carraway, Gatsby's neighbour and Daisy's cousin, narrates the novel retrospectively. He is simultaneously an observer of and participant in Gatsby's world. As a Midwesterner in the East, Nick represents a moral sensibility that contrasts with the careless wealth of the Buchanans.",
   "hint":"GREAT GATSBY narrator = NICK CARRAWAY. Cousin of DAISY, neighbour of GATSBY. NICK = moral observer, outsider from the Midwest. Like Ishmael in Moby-Dick = witness narrator."},

  {"id":20061,"topic":"American Literature","subtopic":"Modernism","difficulty":"medium",
   "q":"Hemingway's 'iceberg theory' (theory of omission) states that:",
   "opts":["A) Stories should begin in medias res","B) The writer should omit what he knows, trusting the reader to feel it","C) Dialogue should always be subtext","D) Prose should use long, flowing sentences to convey depth"],
   "ans":"B","ai_generated":True,
   "explanation":"Hemingway stated in Death in the Afternoon (1932) that a writer who knows enough can omit anything and the reader will still feel it. 'The dignity of movement of an iceberg is due to only one eighth of it being above water.' This justifies his minimalist style.",
   "hint":"HEMINGWAY = ICEBERG = 7/8 hidden. What the writer KNOWS but DOESN'T SAY gives the story its power. Short sentences + omission = reader feels the depth."},

  {"id":20062,"topic":"American Literature","subtopic":"Harlem Renaissance","difficulty":"medium",
   "q":"The term 'New Negro' associated with the Harlem Renaissance was popularised by the anthology edited by:",
   "opts":["A) W.E.B. Du Bois","B) Langston Hughes","C) Alain Locke","D) Marcus Garvey"],
   "ans":"C","ai_generated":True,
   "explanation":"Alain Locke edited The New Negro: An Interpretation (1925), the landmark anthology that defined the Harlem Renaissance. It included essays, poetry, fiction, and art, positioning African-American cultural production as a source of racial pride and aesthetic achievement.",
   "hint":"THE NEW NEGRO anthology (1925) = ALAIN LOCKE (editor). Du Bois wrote The Souls of Black Folk (1903). Hughes wrote poetry. Locke = the PHILOSOPHER of the Harlem Renaissance."},

  {"id":20063,"topic":"American Literature","subtopic":"Poetry","difficulty":"easy",
   "q":"Walt Whitman's Leaves of Grass was first published in:",
   "opts":["A) 1850","B) 1855","C) 1860","D) 1865"],
   "ans":"B","ai_generated":True,
   "explanation":"Whitman published the first edition of Leaves of Grass in 1855 at his own expense — a thin volume of 12 untitled poems including what would later be called 'Song of Myself'. He revised and expanded it through eight editions until 1891-92 ('deathbed edition').",
   "hint":"Whitman LEAVES OF GRASS = 1855 (self-published). He kept revising until death. 1855 = the year before the Civil War tensions peaked (Kansas-Nebraska Act 1854). Free verse = free man."},

  {"id":20064,"topic":"American Literature","subtopic":"Drama","difficulty":"medium",
   "q":"Arthur Miller's Death of a Salesman is a tragedy of:",
   "opts":["A) Classical hubris in a Greek sense","B) The common man who mistakes false dreams for genuine values","C) Political corruption in Cold War America","D) An immigrant's struggle for identity"],
   "ans":"B","ai_generated":True,
   "explanation":"Willy Loman's tragedy is being trapped in the American Dream — the belief that being 'well-liked' and successful in sales is the highest good. Miller argued in 'Tragedy and the Common Man' (1949) that the modern common man can be a tragic hero as validly as any king.",
   "hint":"WILLY LOMAN = LOW MAN (his name suggests his position). DEATH OF A SALESMAN = American Dream is a LIE. Miller: tragedy doesn't need kings — common men can be tragic heroes."},

  # ─── INDIAN LITERATURE ────────────────────────────────────────────────────
  {"id":20070,"topic":"Indian Literature","subtopic":"Fiction","difficulty":"easy",
   "q":"R.K. Narayan's fictional town of Malgudi is modelled on:",
   "opts":["A) Mumbai","B) Mysore/Karnataka region","C) Chennai","D) Kolkata"],
   "ans":"B","ai_generated":True,
   "explanation":"Narayan (1906-2001) based Malgudi on the Mysore region of Karnataka where he lived. It is a quintessentially South Indian small town that serves as the setting for nearly all his novels and stories, including Swami and Friends, The Guide, and The Financial Expert.",
   "hint":"MALGUDI = MYSORE (Karnataka). RK Narayan lived in Mysore. Malgudi = fictional but feels like a real South Indian town. The Guide (1960) = his most celebrated novel, won Sahitya Akademi Award."},

  {"id":20071,"topic":"Indian Literature","subtopic":"Fiction","difficulty":"medium",
   "q":"Mulk Raj Anand's novel Untouchable (1935) depicts one day in the life of:",
   "opts":["A) A Brahmin priest","B) Bakha, a sweeper/latrine cleaner","C) A colonial administrator","D) An Indian soldier in WWI"],
   "ans":"B","ai_generated":True,
   "explanation":"Untouchable follows 18-year-old Bakha, a sweeper, through a single humiliating day in which he accidentally touches a Brahmin and faces violent social ostracism. Anand wrote it to expose the brutality of the caste system; E.M. Forster wrote the preface.",
   "hint":"UNTOUCHABLE (1935) = BAKHA the sweeper. ONE day in his life. Anand + CASTE CRITIQUE. Forster wrote the preface (connecting British and Indian literary worlds)."},

  {"id":20072,"topic":"Indian Literature","subtopic":"Drama","difficulty":"medium",
   "q":"Vijay Tendulkar's play Silence! The Court Is in Session depicts the trial of:",
   "opts":["A) A freedom fighter","B) An unmarried pregnant woman at a mock trial","C) A corrupt judge","D) A Muslim in a Hindu-majority village"],
   "ans":"B","ai_generated":True,
   "explanation":"Silence! The Court Is in Session (1967) presents a seemingly light-hearted amateur theatre group's mock trial that gradually turns into a real lynching of Leela Benare, an unmarried schoolteacher who is pregnant. The play exposes patriarchal hypocrisy and the cruelty of social judgement.",
   "hint":"TENDULKAR 'Silence! The Court Is in Session' = LEELA BENARE on 'trial' for being PREGNANT and unmarried. The mock trial becomes real persecution. Maharashtra's most provocative playwright."},

  {"id":20073,"topic":"Indian Literature","subtopic":"Fiction","difficulty":"hard",
   "q":"Amitav Ghosh's The Shadow Lines (1988) experiments with time and memory by:",
   "opts":["A) Using a non-linear structure where memory challenges national and geographic boundaries","B) Employing a frame narrative of letters between characters","C) Adopting magical realism to describe Partition violence","D) Telling the story through multiple unreliable narrators"],
   "ans":"A","ai_generated":True,
   "explanation":"The Shadow Lines uses an unnamed narrator's memory to move fluidly between Calcutta, London, and Dhaka, and across decades from the 1930s to 1960s. The 'shadow lines' of the title are the arbitrary lines of nations and maps that fail to contain human experience or prevent communal violence.",
   "hint":"SHADOW LINES = lines that are only shadows (not real). National borders are IMAGINARY lines. Ghosh: memory DEFIES geography and time. Non-linear narrative = like actual memory."},

  {"id":20074,"topic":"Indian Literature","subtopic":"Poetry","difficulty":"medium",
   "q":"Kamala Das's confessional poetry collection My Story (1976) was originally written in:",
   "opts":["A) English","B) Malayalam","C) Tamil","D) Hindi"],
   "ans":"B","ai_generated":True,
   "explanation":"My Story (Ente Katha in Malayalam) was originally Kamala Das's autobiography written in Malayalam (1973), later translated into English by the author herself (1976). Her English poetry (Summer in Calcutta, 1965) is equally celebrated for its frank treatment of female sexuality and desire.",
   "hint":"KAMALA DAS wrote in BOTH Malayalam (Madhavikutty) AND English. My Story = Malayalam original 'Ente Katha'. She is Kerala's most celebrated poet in both languages. Important for Kerala SET!"},

  # ─── WORLD LITERATURE ────────────────────────────────────────────────────
  {"id":20080,"topic":"World Literature","subtopic":"African Literature","difficulty":"medium",
   "q":"Ngugi wa Thiong'o's decision to stop writing in English and write only in Gikuyu is articulated in his book:",
   "opts":["A) The River Between","B) Decolonising the Mind (1986)","C) A Grain of Wheat","D) Petals of Blood"],
   "ans":"B","ai_generated":True,
   "explanation":"In Decolonising the Mind: The Politics of Language in African Literature (1986), Ngugi argues that using the coloniser's language perpetuates mental colonisation. He declared it his farewell to English as a literary medium and subsequently wrote in Gikuyu (e.g., Devil on the Cross, Wizard of the Crow).",
   "hint":"NGUGI = DECOLONISING THE MIND (1986). He quit English to write in GIKUYU. Language = political act. Compare: Chinua Achebe chose to stay with English ('It belongs to us too')."},

  {"id":20081,"topic":"World Literature","subtopic":"Caribbean Literature","difficulty":"medium",
   "q":"Derek Walcott's epic poem Omeros (1990) reimagines:",
   "opts":["A) Virgil's Aeneid in a Caribbean setting","B) Homer's Iliad and Odyssey with St Lucian fishermen as characters","C) Shakespeare's The Tempest in Barbados","D) Dante's Inferno in Trinidad"],
   "ans":"B","ai_generated":True,
   "explanation":"Walcott's Omeros transports Homer's characters — Achille, Hector, Helen, Philoctete — to the island of St Lucia, where they are fishermen and local women. The poem meditates on colonial history, Caribbean identity, and the persistence of classical patterns in the postcolonial world.",
   "hint":"WALCOTT OMEROS = Homer's characters in ST LUCIA. Achille (Achilles), Hector, Helen = now Caribbean fishermen. Walcott won Nobel 1992. Omeros = Greek spelling of Homer."},

  {"id":20082,"topic":"World Literature","subtopic":"African Literature","difficulty":"hard",
   "q":"Chimamanda Ngozi Adichie's novel Half of a Yellow Sun (2006) is set during:",
   "opts":["A) The independence of Nigeria (1960)","B) The Biafran War (1967-1970)","C) The colonial period under British rule","D) Contemporary Lagos"],
   "ans":"B","ai_generated":True,
   "explanation":"The novel centres on the Nigerian-Biafran War (1967-70), when Igbo-majority southeastern Nigeria seceded as the Republic of Biafra. The yellow sun of the title refers to the Biafran flag. The war resulted in massive civilian casualties and famine.",
   "hint":"HALF OF A YELLOW SUN = BIAFRAN WAR (1967-70). Yellow sun = Biafran flag symbol. Adichie = Igbo Nigerian writer. Biafra = attempted Igbo secession from Nigeria. Half sun = Biafra's story is unfinished."},

  # ─── LITERARY THEORY ─────────────────────────────────────────────────────
  {"id":20090,"topic":"Literary Theory","subtopic":"New Criticism","difficulty":"easy",
   "q":"The 'intentional fallacy' in New Criticism refers to the mistake of:",
   "opts":["A) Judging a work by its emotional effect on the reader","B) Seeking the author's intention as the standard for interpreting a text","C) Reading literature as historical document","D) Treating all literary forms as equally valuable"],
   "ans":"B","ai_generated":True,
   "explanation":"W.K. Wimsatt and Monroe Beardsley's 'The Intentional Fallacy' (1946) argues that a poem's meaning and success is not determined by what the author intended. The poem becomes public property once written; only the text itself (not the author's mind) can be the standard of criticism.",
   "hint":"INTENTIONAL FALLACY = author's INTENTION is IRRELEVANT. Wimsatt + Beardsley. Partner: AFFECTIVE FALLACY = reader's EMOTION is irrelevant. New Critics care only about THE TEXT."},

  {"id":20091,"topic":"Literary Theory","subtopic":"Structuralism","difficulty":"medium",
   "q":"Roland Barthes's essay 'The Death of the Author' (1967) argues that:",
   "opts":["A) Authors should not be interviewed about their works","B) The birth of the reader must come at the cost of the death of the author","C) Literary authorship is a bourgeois myth to be abolished","D) Only anonymous texts have genuine literary value"],
   "ans":"B","ai_generated":True,
   "explanation":"Barthes argues that once a text is written, the author's intentions become irrelevant; meaning is created by the reader in the act of reading. 'The birth of the reader must be at the cost of the death of the Author.' This is a key post-structuralist move.",
   "hint":"BARTHES 'Death of the Author' = BIRTH OF THE READER. Kill the author = free the text to have multiple meanings. Reader = the one who gives the text meaning. 1967 = same year as Derrida's Of Grammatology."},

  {"id":20092,"topic":"Literary Theory","subtopic":"Postcolonialism","difficulty":"medium",
   "q":"Homi Bhabha's concept of 'mimicry' in colonial discourse refers to:",
   "opts":["A) The colonised imitating the coloniser's culture, producing 'almost the same but not quite'","B) The coloniser's imitation of indigenous customs for administrative purposes","C) The use of parody in anti-colonial literature","D) The way colonial texts copy European literary forms"],
   "ans":"A","ai_generated":True,
   "explanation":"Bhabha argues in The Location of Culture (1994) that colonial mimicry — the colonised subject's imitation of the coloniser — produces an ambivalent 'almost the same but not quite/white' subject who simultaneously confirms and threatens colonial authority. The mimic man is a figure of menace as well as mockery.",
   "hint":"BHABHA MIMICRY = 'almost the same but not QUITE/WHITE'. The colonised copies the coloniser but can never be identical = threatening ambivalence. Think: Macaulay's Indian clerk — English in tastes but never English."},

  {"id":20093,"topic":"Literary Theory","subtopic":"Deconstruction","difficulty":"hard",
   "q":"Derrida's concept of 'différance' (with an 'a') combines the meanings of:",
   "opts":["A) Difference and deference","B) Differing and deferring (of meaning)","C) Differentiation and determination","D) Discourse and reference"],
   "ans":"B","ai_generated":True,
   "explanation":"Derrida coined 'différance' (spelled with 'a' — indistinguishable from 'différence' in French speech, but visible in writing) to capture two simultaneous processes: language works by DIFFERING (each word differs from others) and DEFERRING (meaning is always postponed, never fully present). This undermines the idea of stable, present meaning.",
   "hint":"DIFFÉRANCE (Derrida) = DIFFER + DEFER. Words mean by DIFFERENCE from other words, and meaning is always DEFERRED (never fully arrived). The 'a' is silent in French — only visible in WRITING (ironic for a writing theorist!)."},

  {"id":20094,"topic":"Literary Theory","subtopic":"Feminism","difficulty":"medium",
   "q":"Judith Butler's Gender Trouble (1990) argues that gender is:",
   "opts":["A) A biological fact expressed through cultural behaviour","B) Performative — constituted through repeated acts rather than expressing a prior identity","C) A psychological construct formed in early childhood","D) A social construction that can be abolished through legislation"],
   "ans":"B","ai_generated":True,
   "explanation":"Butler argues that gender has no prior ontological status — there is no 'woman' or 'man' behind the acts. Gender is PERFORMATIVE: it is constituted through repeated, stylised acts (gestures, dress, speech). This does not mean performance is free or voluntary — it is compelled by regulatory norms.",
   "hint":"BUTLER GENDER = PERFORMANCE (not performance as in theatre, but PERFORMATIVE = constituted by acts). 'I do woman' through repeated acts, not 'I am a woman' with a fixed identity. Gender TROUBLE = trouble for the idea of stable gender."},

  {"id":20095,"topic":"Literary Theory","subtopic":"Marxism","difficulty":"medium",
   "q":"Gramsci's concept of 'hegemony' differs from crude Marxist base-superstructure theory because it emphasises:",
   "opts":["A) Economic determination as the only cause of ideology","B) Consent and cultural leadership rather than coercion alone","C) The role of the state in directly controlling consciousness","D) Class struggle as the only means of social change"],
   "ans":"B","ai_generated":True,
   "explanation":"Gramsci, writing in his Prison Notebooks (1929-35), argued that ruling class power is sustained not merely by force but through 'hegemony' — cultural and intellectual leadership that makes the dominated class consent to their own domination. This requires the 'organic intellectual' as a counter-hegemonic force.",
   "hint":"GRAMSCI HEGEMONY = power through CONSENT not just force. The ruling class 'leads' culturally, not just politically. Counter-hegemony needs ORGANIC INTELLECTUALS (from the working class). Hegemony ≠ army; hegemony = ideas everyone 'agrees' with."},

  {"id":20096,"topic":"Literary Theory","subtopic":"Psychoanalytic Criticism","difficulty":"hard",
   "q":"Lacan's Mirror Stage theory argues that the infant's first recognition of its image in the mirror produces:",
   "opts":["A) A secure, unified sense of self","B) A misrecognition (méconnaissance) — an idealized, alienated image of a coherent self","C) The infant's entry into the Symbolic order of language","D) The formation of the superego"],
   "ans":"B","ai_generated":True,
   "explanation":"Lacan's Mirror Stage (6-18 months) produces not a true self but a misrecognition (méconnaissance): the infant sees its reflection as a coherent, unified whole, which is actually an external, alien image. This alienated identification becomes the foundation of the ego — forever a fiction, always other.",
   "hint":"LACAN MIRROR STAGE = MISRECOGNITION (méconnaissance). Baby sees itself as WHOLE in mirror but it's just an IMAGE = alienated. Ego = always a fiction, always other. Then later = SYMBOLIC order (language)."},

  {"id":20097,"topic":"Literary Theory","subtopic":"New Historicism","difficulty":"medium",
   "q":"Stephen Greenblatt's concept of 'self-fashioning' in Renaissance Self-Fashioning (1980) argues that:",
   "opts":["A) Renaissance individuals had complete freedom to construct their identities","B) Identity in the Renaissance was formed through submission to authority as much as self-construction","C) Renaissance literature rejected all social constraints on individual expression","D) The self was irrelevant in Renaissance humanism"],
   "ans":"B","ai_generated":True,
   "explanation":"Greenblatt shows that Renaissance self-fashioning — the construction of a public identity — always involved submission to an authority (God, a monarch, a text) and the definition of self against an Other (heretic, alien, woman). Freedom and constraint are simultaneously present.",
   "hint":"GREENBLATT SELF-FASHIONING = identity made through SUBMISSION as much as freedom. You fashion yourself AGAINST a threatening Other. New Historicism: power is everywhere in culture, not just politics."},

  # ─── LINGUISTICS ─────────────────────────────────────────────────────────
  {"id":20100,"topic":"Linguistics","subtopic":"Phonetics","difficulty":"medium",
   "q":"Which of the following is a voiced bilabial plosive?",
   "opts":["A) /p/","B) /b/","C) /m/","D) /f/"],
   "ans":"B","ai_generated":True,
   "explanation":"/b/ is voiced (vocal cords vibrate), bilabial (both lips), and plosive (complete closure then release). /p/ is voiceless bilabial plosive. /m/ is voiced bilabial NASAL (air through nose). /f/ is voiceless labiodental fricative.",
   "hint":"VOICED BILABIAL PLOSIVE = /b/. Minimal pair: /p/ (voiceless) vs /b/ (voiced) — same place (bilabial) and manner (plosive), differ only in VOICING. Put your hand on your throat: /b/ buzzes, /p/ doesn't."},

  {"id":20101,"topic":"Linguistics","subtopic":"Semantics","difficulty":"medium",
   "q":"The semantic relation between 'scarlet', 'crimson', and 'vermilion' is an example of:",
   "opts":["A) Antonymy","B) Synonymy","C) Hyponymy — all are hyponyms of 'red'","D) Polysemy"],
   "ans":"C","ai_generated":True,
   "explanation":"Scarlet, crimson, and vermilion are all specific types (hyponyms) of the superordinate term 'red'. The relation is: red is the HYPERNYM; scarlet/crimson/vermilion are CO-HYPONYMS of red. They are not synonyms (they are distinct shades) nor antonyms.",
   "hint":"HYPONYMY = X is a kind of Y. Scarlet is a kind of RED. Red = hypernym (superordinate). Scarlet/crimson/vermilion = co-hyponyms. Think: PET is hypernym of DOG/CAT/BIRD (they are co-hyponyms of pet)."},

  {"id":20102,"topic":"Linguistics","subtopic":"Pragmatics","difficulty":"medium",
   "q":"According to Austin's speech act theory, a performative utterance is one that:",
   "opts":["A) Merely describes a state of affairs","B) Performs the action it names when uttered in appropriate conditions","C) Always requires a response from the listener","D) Can only be made by authorised speakers in formal contexts"],
   "ans":"B","ai_generated":True,
   "explanation":"Austin (How to Do Things with Words, 1962) distinguished constatives (descriptions, true or false) from performatives (utterances that DO something: 'I promise', 'I hereby sentence you', 'I do'). A performative is felicitous (not true/false) when conditions are right.",
   "hint":"AUSTIN PERFORMATIVE = utterance that DOES what it says. 'I promise' = the ACT of promising. 'I now pronounce you married' = performs marriage. Not true/false — FELICITOUS or INFELICITOUS (happy or unhappy conditions)."},

  {"id":20103,"topic":"Linguistics","subtopic":"Morphology","difficulty":"easy",
   "q":"The process by which words like 'brunch' (breakfast + lunch) or 'smog' (smoke + fog) are formed is called:",
   "opts":["A) Compounding","B) Affixation","C) Blending","D) Conversion"],
   "ans":"C","ai_generated":True,
   "explanation":"Blending (also called portmanteau words) combines parts of two words: br(eakfast) + (l)unch = brunch; sm(oke) + (f)og = smog. This differs from compounding (which combines two complete words: blackbird) and affixation (which adds a bound morpheme).",
   "hint":"BLENDING = parts of two words FUSED. brunch = br+unch, smog = sm+og. Also: blog (web+log), motel (motor+hotel), Brexit (Britain+exit). Different from COMPOUND (full words: blackbird, toothpaste)."},

  {"id":20104,"topic":"Linguistics","subtopic":"Sociolinguistics","difficulty":"medium",
   "q":"Diglossia, as defined by Charles Ferguson (1959), refers to:",
   "opts":["A) Bilingualism in an individual","B) Two varieties of the same language used for different social functions (H and L varieties)","C) The mixing of two different languages in a single utterance","D) The use of multiple dialects in literary writing"],
   "ans":"B","ai_generated":True,
   "explanation":"Ferguson defined diglossia as the situation where a speech community uses two varieties (HIGH and LOW) of the same language for distinct social functions: H (formal, religious, literary) and L (informal, everyday). Example: Classical Arabic (H) vs. colloquial Arabic dialects (L).",
   "hint":"DIGLOSSIA = TWO varieties, same language, different FUNCTIONS. H = High (formal, religious). L = Low (home, market). Ferguson (1959). Greek: dí (two) + glōssa (tongue). Not bilingualism (two different languages) — diglossia (two registers of ONE language)."},

  {"id":20105,"topic":"Linguistics","subtopic":"Language Acquisition","difficulty":"medium",
   "q":"Krashen's distinction between 'acquisition' and 'learning' holds that:",
   "opts":["A) Children acquire L1 but must formally learn L2","B) Acquisition is subconscious (natural communication); learning is conscious (rule study)","C) Adults can only learn, not acquire, a second language","D) Learning leads to fluency faster than acquisition"],
   "ans":"B","ai_generated":True,
   "explanation":"Krashen's Acquisition-Learning Hypothesis (Input Hypothesis, 1985) distinguishes subconscious acquisition (like a child picking up L1 through natural communication) from conscious learning (studying grammar rules). Acquired knowledge enables fluency; learned knowledge can only monitor output.",
   "hint":"KRASHEN: ACQUISITION (subconscious, natural) vs LEARNING (conscious, rules). Children ACQUIRE language naturally. Adults often LEARN rules but can't speak fluently. Krashen prefers COMPREHENSIBLE INPUT (i+1) over drilling."},

  {"id":20106,"topic":"Linguistics","subtopic":"Historical Linguistics","difficulty":"medium",
   "q":"Grimm's Law (First Germanic Consonant Shift) explains why Latin 'pater' corresponds to English 'father'. The sound change involved is:",
   "opts":["A) Voiced stops become voiceless","B) Voiceless stops become voiceless fricatives (p→f, t→θ, k→h)","C) Nasals become plosives","D) Fricatives become stops"],
   "ans":"B","ai_generated":True,
   "explanation":"Grimm's Law (1822) describes a systematic shift: PIE voiceless stops (p, t, k) became Germanic voiceless fricatives (f, θ, h). So Latin/PIE *p becomes English f: pater→father, piscis→fish, ped-→foot. This shows the Germanic languages (including English) underwent a unique consonant shift.",
   "hint":"GRIMM'S LAW: p→f, t→θ (th), k→h. Latin pater = English FATHER (p→f). Latin tres = English THREE (t→th). Latin cornu = English HORN (k→h). Discovered by Jacob Grimm (same Grimm as fairy tales!)."},
]

# Mark all as ai_generated
for q in PRELOADED_QUESTIONS:
    q.setdefault("ai_generated", True)
    q.setdefault("explanation", "")
    q.setdefault("hint", "")

MEGA_PROMPT_TEMPLATE = """You are a senior question setter for the Kerala SET exam in English Language and Literature, with 20 years of UGC-style MCQ experience.

Generate exactly {count} high-quality, original MCQ questions.

SPECIFICATIONS:
Topic: {topic} | Subtopic: {subtopic} | Difficulty: {difficulty}
Style: {q_type} | Angle: {angle}
Scope: {context}

STRICT RULES:
1. Each question: exactly 4 options A) B) C) D)
2. Exactly ONE correct answer
3. Distractors must use real authors/works/terms but be clearly wrong to a prepared candidate
4. Do NOT rephrase or repeat: {existing_sample}
5. Include 'explanation': 2-3 sentences — WHY correct, why each distractor wrong
6. Include 'hint': one-sentence mnemonic or memory hook
7. Hard = nuanced specialist knowledge; Easy = canonical must-know facts

OUTPUT: Respond with ONLY valid JSON (no markdown, no text outside JSON):
{{"questions":[{{"q":"Question?","opts":["A) opt","B) opt","C) opt","D) opt"],"ans":"B","topic":"{topic}","subtopic":"{subtopic}","difficulty":"{difficulty}","explanation":"Correct because... A is wrong because... C is wrong because...","hint":"Remember: ..."}}]}}"""

DISCUSSION_PROMPT = """You are a brilliant, encouraging English Literature professor guiding a Kerala SET aspirant who got a question WRONG.

QUESTION: {question}
ALL OPTIONS:
{options}
CORRECT ANSWER: {correct_opt}
STUDENT CHOSE: {student_opt}

Write a warm, detailed tutorial covering:
**1. Why the correct answer is right** — explain deeply with historical/literary context
**2. Why the student's choice was wrong** — address the misconception directly
**3. Key facts to memorise** — 4-5 bullet points essential for SET
**4. Two related SET-style questions** on the same topic (with answers)
**5. Memory trick** — a mnemonic or unforgettable hook

Be encouraging, thorough, and specific. Write as if in a face-to-face tutorial session."""

EXPLAIN_PROMPT = """You are an expert Kerala SET English Literature tutor.

Explain this question for a student who wants to understand it deeply:

QUESTION: {question}
CORRECT ANSWER: {correct_opt}
TOPIC: {topic} — {subtopic}

Cover:
1. **Core concept** in simple, clear terms
2. **Why each option** is right or wrong
3. **Context**: literary period, movement, critical significance
4. **Exam pattern**: what kind of SET question uses this knowledge
5. **3 quick related facts** that could appear in the same question area

Keep under 300 words. Be precise, engaging, and educational."""


def _call_claude(api_key, prompt, max_tokens=8192):
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=AI_MODEL, max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip()


def _parse_questions_json(raw, topic, subtopic, difficulty):
    raw_clean = re.sub(r"```(?:json)?\s*", "", raw)
    raw_clean = re.sub(r"\s*```", "", raw_clean).strip()
    m = re.search(r"\{.*\}", raw_clean, re.DOTALL)
    if not m:
        return []
    try:
        data = json.loads(m.group())
    except Exception:
        return []
    questions = data.get("questions", [])
    start_id = 100000 + random.randint(1000, 899000)
    valid = []
    for i, q in enumerate(questions):
        q["id"] = start_id + i
        q["ai_generated"] = True
        q.setdefault("explanation", "")
        q.setdefault("hint", "")
        q.setdefault("tags", [topic, subtopic])
        if (all(k in q for k in ["q", "opts", "ans"])
                and len(q["opts"]) == 4
                and q["ans"] in ["A", "B", "C", "D"]):
            valid.append(q)
    return valid


def generate_questions_ai(api_key, topic, subtopic, difficulty, count=10, existing=None):
    if not existing: existing = []
    q_type   = random.choice(QUESTION_TYPES)
    angle    = random.choice(ANGLES)
    context  = AI_TOPIC_PROMPTS.get(topic, topic)
    ex_sample = "\n".join(f"- {q}" for q in existing[:6]) if existing else "(none yet)"
    prompt = MEGA_PROMPT_TEMPLATE.format(
        count=count, topic=topic, subtopic=subtopic, difficulty=difficulty,
        q_type=q_type, angle=angle, context=context, existing_sample=ex_sample
    )
    raw = _call_claude(api_key, prompt, max_tokens=8192)
    return _parse_questions_json(raw, topic, subtopic, difficulty)


def generate_batch_smart(api_key, topics, difficulties, total_count,
                          existing=None, progress_cb=None):
    if not existing: existing = []
    topic_weights = {"British Literature":3,"Literary Theory":3,"Linguistics":2,
                     "Indian Literature":2,"American Literature":1,"World Literature":1}
    combos = []
    for t in topics:
        w = topic_weights.get(t, 1)
        for d in difficulties:
            combos.extend([(t, d)] * w)
    random.shuffle(combos)
    per_call = max(8, min(15, total_count // max(1, len(combos))))
    all_new, errors = [], []
    for idx, (topic, diff) in enumerate(combos):
        if len(all_new) >= total_count: break
        remaining = total_count - len(all_new)
        n = min(per_call, remaining)
        if n <= 0: break
        subtopic = random.choice(SUBTOPIC_MAP.get(topic, [topic]))
        try:
            new_qs = generate_questions_ai(api_key, topic, subtopic, diff, count=n, existing=existing)
            all_new.extend(new_qs)
            existing.extend([q["q"] for q in new_qs])
        except anthropic.BadRequestError as e:
            if "credit" in str(e).lower() or "balance" in str(e).lower():
                raise ValueError("CREDITS")
            errors.append(f"{topic}/{diff}: {str(e)[:80]}")
        except anthropic.AuthenticationError:
            raise ValueError("AUTHFAIL")
        except anthropic.RateLimitError:
            raise ValueError("RATELIMIT")
        except Exception as e:
            errors.append(f"{topic}/{diff}: {str(e)[:80]}")
        if progress_cb: progress_cb(idx + 1, len(combos), len(all_new), errors)
    return all_new, errors


def get_discussion(api_key, question, options, correct_opt, student_opt):
    prompt = DISCUSSION_PROMPT.format(
        question=question,
        options="\n".join(options),
        correct_opt=correct_opt,
        student_opt=student_opt
    )
    return _call_claude(api_key, prompt, max_tokens=1500)


def get_explanation(api_key, question, correct_opt, topic, subtopic):
    prompt = EXPLAIN_PROMPT.format(
        question=question, correct_opt=correct_opt,
        topic=topic, subtopic=subtopic
    )
    return _call_claude(api_key, prompt, max_tokens=1000)


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
#  PAGE: AI GENERATOR  (rebuilt v3)
# ══════════════════════════════════════════════════════════════════════════════

def page_ai_gen():
    st.markdown("""<div class="app-hdr">
    <div><h1>🤖 AI Question Generator & Discussion Centre</h1>
    <div class="sub">300+ pre-loaded questions with explanations · AI tutor · Discussion mode · Bulk generation</div></div>
    <div class="bdg">Powered by Claude</div></div>""",unsafe_allow_html=True)

    # ── Hero Banner ──────────────────────────────────────────────────────────
    ai_c   = len(st.session_state.ai_questions)
    pre_c  = len(PRELOADED_QUESTIONS)
    total  = len(QUESTION_BANK) + pre_c + ai_c
    with_exp = len([q for q in PRELOADED_QUESTIONS + st.session_state.ai_questions if q.get("explanation")])

    st.markdown(f"""<div style="background:linear-gradient(135deg,#0d2347 0%,#1a3a6b 60%,#1565c0 100%);
    border-radius:16px;padding:1.6rem 2rem;margin-bottom:1.2rem;
    box-shadow:0 8px 32px rgba(26,58,107,.35)">
    <div style="display:flex;align-items:center;gap:1.5rem;flex-wrap:wrap;margin-bottom:1rem">
      <div style="font-size:2.8rem">⚡</div>
      <div>
        <div style="font-family:Playfair Display,serif;font-size:1.3rem;font-weight:700;color:#fff">
          Permutation × Combination Engine</div>
        <div style="font-size:.84rem;opacity:.82;color:#fff;margin-top:.2rem">
          {pre_c} pre-loaded expert questions + API generation + Full explanation & discussion on every question
        </div>
      </div>
    </div>
    <div style="display:flex;gap:10px;flex-wrap:wrap">
      <div style="background:rgba(255,255,255,.15);border-radius:8px;padding:8px 14px;font-size:.78rem;color:#fff">
        📦 {total} Total Questions</div>
      <div style="background:rgba(255,255,255,.15);border-radius:8px;padding:8px 14px;font-size:.78rem;color:#fff">
        📖 {with_exp} With Full Explanations</div>
      <div style="background:rgba(255,255,255,.15);border-radius:8px;padding:8px 14px;font-size:.78rem;color:#fff">
        💬 Discussion on Every Question</div>
      <div style="background:rgba(255,255,255,.15);border-radius:8px;padding:8px 14px;font-size:.78rem;color:#fff">
        🤖 {ai_c} API-Generated</div>
    </div></div>""",unsafe_allow_html=True)

    stat_cards([
        ("Seed Questions",  len(QUESTION_BANK),  "sc-blue"),
        ("Pre-loaded Expert Qs", pre_c,           "sc-green"),
        ("API Generated",   ai_c,                 "sc-gold"),
        ("Total Bank",      total,                "sc-red"),
    ])

    tab1, tab2, tab3, tab4 = st.tabs([
        "🚀 Generate More", "📋 Browse Questions", "💬 Discussion Centre", "📊 Matrix"
    ])

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 1: Generate
    # ══════════════════════════════════════════════════════════════════════════
    with tab1:
        has_key = bool(st.session_state.api_key)

        if not has_key:
            st.markdown("""<div style="background:#e3f2fd;border-radius:14px;padding:1.5rem 1.8rem;
            border-left:5px solid #1565c0;margin-bottom:1rem">
            <div style="font-weight:700;color:#0d47a1;font-size:1rem;margin-bottom:.5rem">
              ℹ️ 300+ Questions Already Loaded!</div>
            <div style="color:#1a237e;font-size:.88rem;line-height:1.7">
              You already have <strong>300+ pre-loaded expert questions</strong> with full explanations and hints
              ready to use in the <strong>Browse</strong> and <strong>Discussion</strong> tabs — no API key needed!<br><br>
              To generate <em>additional</em> AI questions, enter your Anthropic API key in the sidebar.<br>
              Get one free at: <strong>console.anthropic.com</strong> → API Keys (free tier available)
            </div></div>""",unsafe_allow_html=True)
        else:
            # Credit status check
            st.markdown("""<div style="background:#e8f5e9;border-radius:10px;padding:.8rem 1.2rem;
            border-left:4px solid #27ae60;margin-bottom:.8rem;font-size:.85rem;color:#1b5e20">
            ✅ API key detected — ready to generate additional questions
            </div>""",unsafe_allow_html=True)

        st.markdown("### ⚙️ Generation Settings")
        col1, col2 = st.columns(2)
        with col1:
            sel_topics = st.multiselect("Topics", TOPICS, default=TOPICS, key="gen_t")
            sel_diffs  = st.multiselect("Difficulty levels", DIFFICULTIES, default=DIFFICULTIES, key="gen_d")
        with col2:
            n_q = st.slider("Questions to generate", 20, 300, 50, step=10, key="gen_n",
                            help="Each API call produces 10–15 Qs. 100 questions ≈ 7–10 API calls.")
            combos = len(sel_topics) * len(sel_diffs)
            if combos:
                calls_est = max(1, n_q // 12)
                cost_est  = calls_est * 0.003
                st.markdown(f"""<div style="background:#e3f2fd;border-radius:8px;padding:10px 14px;
                font-size:.83rem;color:#0d47a1">
                📐 <strong>{combos*3}</strong> topic×difficulty combos<br>
                ⚡ ~<strong>{calls_est}</strong> API calls (12 Qs each)<br>
                💰 Estimated cost: ~<strong>${cost_est:.2f}</strong>
                </div>""",unsafe_allow_html=True)

        st.markdown("---")
        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1:
            go_btn = st.button("🚀 Generate with AI",type="primary",use_container_width=True,key="gen_go",
                               disabled=not has_key)
        with col_b2:
            quick_btn = st.button("⚡ Quick 50 — British Lit",use_container_width=True,key="gen_quick",
                                  disabled=not has_key)
        with col_b3:
            theory_btn = st.button("🧠 50 Theory Questions",use_container_width=True,key="gen_theory",
                                   disabled=not has_key)

        if not has_key:
            st.info("🔑 Add API key in sidebar to enable generation. Browse pre-loaded questions meanwhile!")
        else:
            sel_topics_r = sel_diffs_r = None; n_q_r = n_q
            if go_btn:     sel_topics_r, sel_diffs_r = sel_topics, sel_diffs
            elif quick_btn: sel_topics_r, sel_diffs_r, n_q_r = ["British Literature"], DIFFICULTIES, 50
            elif theory_btn: sel_topics_r, sel_diffs_r, n_q_r = ["Literary Theory"], DIFFICULTIES, 50

            if sel_topics_r:
                if not sel_topics_r:
                    st.error("Select at least one topic."); st.stop()
                existing_qs = [q["q"] for q in all_questions()]
                prog_hdr = st.empty()
                prog_bar = st.progress(0)
                prog_stats = st.empty()
                prog_log   = st.empty()
                err_box    = st.empty()
                prog_hdr.markdown("### ⏳ Generating…")
                log_lines = []

                def update_progress(done, total_combos, n_gen, errors):
                    pct = min(99, int(done/total_combos*100))
                    prog_bar.progress(pct)
                    prog_stats.markdown(f"""<span style="color:#1a3a6b;font-weight:600">
                    📦 {n_gen} generated</span>  |  Combo {done}/{total_combos}""",
                    unsafe_allow_html=True)
                    if done % 3 == 0:
                        log_lines.append(f"✅ Combo {done}: {n_gen} total")
                        prog_log.text("\n".join(log_lines[-4:]))

                try:
                    new_qs, errors = generate_batch_smart(
                        st.session_state.api_key, sel_topics_r, sel_diffs_r,
                        n_q_r, existing=existing_qs, progress_cb=update_progress)
                    prog_bar.progress(100); prog_hdr.empty(); prog_log.empty(); prog_stats.empty()
                    if new_qs:
                        st.session_state.ai_questions.extend(new_qs)
                        st.markdown(f"""<div style="background:linear-gradient(135deg,#1b5e20,#27ae60);
                        border-radius:14px;padding:1.5rem 2rem;color:#fff;text-align:center;
                        box-shadow:0 6px 24px rgba(39,174,96,.3)">
                        <div style="font-size:2.5rem;font-weight:800;color:#fff">{len(new_qs)}</div>
                        <div style="font-size:1rem;color:#fff;opacity:.9">Questions Generated!</div>
                        <div style="font-size:.82rem;color:#fff;opacity:.72;margin-top:.3rem">
                          Total: {len(QUESTION_BANK)+len(PRELOADED_QUESTIONS)+len(st.session_state.ai_questions)}
                        </div></div>""",unsafe_allow_html=True)
                        st.balloons()
                        if errors:
                            with st.expander(f"⚠️ {len(errors)} warnings"):
                                for e in errors: st.text(e)
                    else:
                        err_box.error("No questions generated. Check settings.")
                except ValueError as e:
                    prog_bar.empty(); prog_hdr.empty()
                    err_str = str(e)
                    if err_str == "CREDITS":
                        err_box.markdown("""<div style="background:#fce4ec;border-radius:12px;
                        padding:1.5rem;border-left:5px solid #c0392b">
                        <div style="font-weight:700;color:#b71c1c;font-size:1rem">💳 No API Credits</div>
                        <div style="color:#7f0000;font-size:.88rem;margin-top:.5rem;line-height:1.7">
                        Your Anthropic account needs credits. Add at <strong>console.anthropic.com → Billing</strong>.<br>
                        Generating 100 questions ≈ <strong>$0.02–$0.05</strong> (very cheap!)<br>
                        <strong>Meanwhile: use the 300+ pre-loaded questions in Browse tab!</strong>
                        </div></div>""",unsafe_allow_html=True)
                    elif err_str == "AUTHFAIL":
                        err_box.error("🔑 Invalid API key. Check sidebar.")
                    elif err_str == "RATELIMIT":
                        err_box.warning("⏱️ Rate limit hit. Wait 60 seconds.")
                    else:
                        err_box.error(f"❌ {err_str}")
                except Exception as e:
                    prog_bar.empty(); prog_hdr.empty()
                    err_box.error(f"❌ Unexpected error: {str(e)}")

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 2: Browse Questions
    # ══════════════════════════════════════════════════════════════════════════
    with tab2:
        browse_pool = PRELOADED_QUESTIONS + st.session_state.ai_questions
        st.markdown(f"### 📋 Browsing {len(browse_pool)} Expert Questions")

        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        with col_f1: bf_t = st.selectbox("Topic",["All"]+TOPICS,key="bf_t")
        with col_f2: bf_d = st.selectbox("Difficulty",["All"]+DIFFICULTIES,key="bf_d")
        with col_f3: bf_s = st.selectbox("Source",["All","Pre-loaded","API Generated"],key="bf_s")
        with col_f4: bf_q = st.text_input("Search",placeholder="keyword…",key="bf_q")

        filtered = browse_pool
        if bf_t != "All": filtered = [q for q in filtered if q.get("topic")==bf_t]
        if bf_d != "All": filtered = [q for q in filtered if q.get("difficulty")==bf_d]
        if bf_s == "Pre-loaded": filtered = [q for q in filtered if q["id"] < 90000]
        elif bf_s == "API Generated": filtered = [q for q in filtered if q["id"] >= 90000]
        if bf_q:
            kw = bf_q.lower()
            filtered = [q for q in filtered if kw in q["q"].lower() or
                       any(kw in o.lower() for o in q["opts"]) or
                       kw in q.get("explanation","").lower()]

        st.markdown(f"**{len(filtered)}** questions match your filters")
        st.markdown("---")

        PAGE_SIZE = 10
        total_pages = max(1, (len(filtered)+PAGE_SIZE-1)//PAGE_SIZE)
        page_num = st.number_input("Page", 1, total_pages, 1, key="bf_page")

        for q in filtered[(page_num-1)*PAGE_SIZE : page_num*PAGE_SIZE]:
            dc    = q.get("difficulty","medium")
            dc_col= {"easy":"#27ae60","medium":"#2980b9","hard":"#c0392b"}.get(dc,"#666")
            has_expl = bool(q.get("explanation"))
            has_hint = bool(q.get("hint"))
            badges = ""
            if has_expl: badges += ' <span style="background:#e8f5e9;color:#1b5e20;font-size:.65rem;font-weight:700;padding:1px 7px;border-radius:10px">📖 EXPLANATION</span>'
            if has_hint: badges += ' <span style="background:#fff8e1;color:#8a6200;font-size:.65rem;font-weight:700;padding:1px 7px;border-radius:10px">💡 HINT</span>'

            with st.expander(f"[{dc.upper()}] {q['q'][:95]}{'...' if len(q['q'])>95 else ''}"):
                st.markdown(f"""<div style="background:#f8faff;border-radius:10px;padding:1rem 1.2rem;margin-bottom:.6rem">
                <div style="display:flex;gap:6px;margin-bottom:.7rem;flex-wrap:wrap">
                  <span style="background:#e8eef7;color:#1a3a6b;font-size:.68rem;font-weight:700;padding:2px 9px;border-radius:12px">{q.get("topic","")}</span>
                  <span style="background:#e8eef7;color:#1a3a6b;font-size:.68rem;font-weight:700;padding:2px 9px;border-radius:12px">{q.get("subtopic","")}</span>
                  <span style="background:{dc_col}22;color:{dc_col};font-size:.68rem;font-weight:700;padding:2px 9px;border-radius:12px">{dc.upper()}</span>
                  {badges}
                </div>
                <div style="font-size:.98rem;font-weight:600;color:#1c1c2e;margin-bottom:.9rem;line-height:1.6">{q["q"]}</div>""",
                unsafe_allow_html=True)

                for opt in q["opts"]:
                    is_a = opt[0] == q["ans"]
                    st.markdown(f"""<div style="background:{"#eafaf1" if is_a else "#f8faff"};
                    border:1.5px solid {"#27ae60" if is_a else "#dce3ee"};border-radius:8px;
                    padding:7px 13px;margin-bottom:5px;font-size:.89rem;
                    color:{"#1b5e20" if is_a else "#2c2c3e"};
                    font-weight:{"700" if is_a else "400"}">{"✅" if is_a else "  "} {opt}</div>""",
                    unsafe_allow_html=True)
                st.markdown("</div>",unsafe_allow_html=True)

                if q.get("explanation"):
                    st.markdown(f"""<div style="background:#e8f5e9;border-radius:9px;padding:.9rem 1.1rem;
                    margin-top:.5rem;border-left:4px solid #27ae60">
                    <div style="font-size:.7rem;font-weight:700;color:#1b5e20;text-transform:uppercase;letter-spacing:.5px;margin-bottom:.3rem">📖 Explanation</div>
                    <div style="font-size:.87rem;color:#1c2c1e;line-height:1.65">{q["explanation"]}</div></div>""",
                    unsafe_allow_html=True)

                if q.get("hint"):
                    st.markdown(f"""<div style="background:#fff8e1;border-radius:9px;padding:.7rem 1.1rem;
                    margin-top:.5rem;border-left:4px solid #f39c12">
                    <div style="font-size:.7rem;font-weight:700;color:#8a6200;text-transform:uppercase;letter-spacing:.5px;margin-bottom:.2rem">💡 Memory Hint</div>
                    <div style="font-size:.85rem;color:#5a4000;line-height:1.55">{q["hint"]}</div></div>""",
                    unsafe_allow_html=True)

                # Discussion shortcut
                st.markdown("<div style='height:.5rem'></div>",unsafe_allow_html=True)
                c_disc, c_quiz = st.columns(2)
                with c_disc:
                    if st.button("💬 Discuss This Question",key=f"disc_{q['id']}",use_container_width=True):
                        st.session_state["disc_q_id"] = q["id"]
                        st.session_state.page = "ai_gen"
                        # Jump to discussion tab by storing state
                        st.session_state["active_tab"] = "discussion"
                        st.rerun()
                with c_quiz:
                    if st.button("📝 Quiz This Topic",key=f"qtopic_{q['id']}",use_container_width=True):
                        start_quiz(topic_filter=[q.get("topic")],count=15)
                        st.session_state.page="quiz"; st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 3: Discussion Centre
    # ══════════════════════════════════════════════════════════════════════════
    with tab3:
        st.markdown("""<div style="background:linear-gradient(135deg,#1a3a6b,#0d47a1);
        border-radius:14px;padding:1.4rem 1.6rem;margin-bottom:1.2rem">
        <div style="font-size:1.2rem;font-weight:700;color:#fff;margin-bottom:.4rem">
          💬 AI Discussion & Explanation Centre</div>
        <div style="font-size:.85rem;color:rgba(255,255,255,.82);line-height:1.6">
          Select any question · Choose your answer · Get a detailed professor-style tutorial<br>
          Works on all 300+ pre-loaded questions. Claude AI gives deeper explanations when API key is available.
        </div></div>""",unsafe_allow_html=True)

        # ── Question selector ────────────────────────────────────────────────
        disc_pool = all_questions()
        col_d1, col_d2, col_d3 = st.columns([2,1,1])
        with col_d1: disc_topic = st.selectbox("Filter by topic",["All"]+TOPICS,key="disc_t")
        with col_d2: disc_diff  = st.selectbox("Difficulty",["All"]+DIFFICULTIES,key="disc_d")
        with col_d3: disc_src   = st.selectbox("Source",["All","Has Explanation","Has Hint"],key="disc_src")

        pool_f = disc_pool
        if disc_topic != "All": pool_f = [q for q in pool_f if q.get("topic")==disc_topic]
        if disc_diff  != "All": pool_f = [q for q in pool_f if q.get("difficulty")==disc_diff]
        if disc_src == "Has Explanation": pool_f = [q for q in pool_f if q.get("explanation")]
        elif disc_src == "Has Hint":      pool_f = [q for q in pool_f if q.get("hint")]

        if not pool_f:
            st.info("No questions match this filter."); 
        else:
            # Build question options
            q_labels = {q["id"]: f"[{q.get('difficulty','?').upper()}] {q['q'][:80]}..." for q in pool_f}
            
            # Check if a question was pre-selected from Browse
            pre_sel_id = st.session_state.get("disc_q_id", None)
            pre_sel_idx = 0
            if pre_sel_id:
                ids = list(q_labels.keys())
                if pre_sel_id in ids:
                    pre_sel_idx = ids.index(pre_sel_id)

            sel_id = st.selectbox(
                f"Select question ({len(pool_f)} available)",
                options=list(q_labels.keys()),
                format_func=lambda x: q_labels[x],
                index=pre_sel_idx,
                key="disc_sel"
            )

            sel_q = next((q for q in pool_f if q["id"]==sel_id), None)
            if not sel_q:
                st.warning("Question not found."); 
            else:
                st.markdown("---")
                # Show question card
                dc = sel_q.get("difficulty","medium")
                dc_col = {"easy":"#27ae60","medium":"#2980b9","hard":"#c0392b"}.get(dc,"#666")
                st.markdown(f"""<div style="background:#ffffff;border-radius:14px;padding:1.5rem 1.8rem;
                box-shadow:0 4px 20px rgba(0,0,0,.09);border:2px solid {dc_col}33;margin-bottom:1rem">
                <div style="display:flex;gap:6px;margin-bottom:.6rem">
                  <span style="background:#e8eef7;color:#1a3a6b;font-size:.68rem;font-weight:700;padding:2px 9px;border-radius:12px">{sel_q.get("topic","")}</span>
                  <span style="background:{dc_col}22;color:{dc_col};font-size:.68rem;font-weight:700;padding:2px 9px;border-radius:12px">{dc.upper()}</span>
                </div>
                <div style="font-size:1.05rem;font-weight:600;color:#1c1c2e;line-height:1.65;margin-bottom:1rem">{sel_q["q"]}</div>
                </div>""",unsafe_allow_html=True)

                # ── Answer selection ─────────────────────────────────────────
                st.markdown("**Choose your answer:**")
                opt_labels = {opt[0]: opt for opt in sel_q["opts"]}
                user_choice = st.radio("",
                    options=list(opt_labels.keys()),
                    format_func=lambda x: opt_labels[x],
                    key=f"disc_ans_{sel_q['id']}",
                    horizontal=False)

                st.markdown("<div style='height:.5rem'></div>",unsafe_allow_html=True)
                col_sub, col_exp = st.columns(2)
                with col_sub:
                    submit_disc = st.button("✅ Submit & Discuss",type="primary",
                                           use_container_width=True,key=f"disc_sub_{sel_q['id']}")
                with col_exp:
                    explain_only = st.button("📖 Explain Correct Answer",
                                            use_container_width=True,key=f"disc_expl_{sel_q['id']}")

                # ── Discussion output ────────────────────────────────────────
                if submit_disc or explain_only:
                    correct_letter = sel_q["ans"]
                    correct_opt = next(o for o in sel_q["opts"] if o[0]==correct_letter)
                    user_opt    = opt_labels.get(user_choice,"")
                    is_correct  = user_choice == correct_letter

                    if submit_disc:
                        # Result feedback
                        if is_correct:
                            st.markdown(f"""<div style="background:linear-gradient(135deg,#1b5e20,#27ae60);
                            border-radius:12px;padding:1.2rem 1.5rem;margin:.8rem 0;color:#fff;text-align:center">
                            <div style="font-size:2rem">🎉</div>
                            <div style="font-size:1.1rem;font-weight:700;color:#fff">Correct!</div>
                            <div style="font-size:.85rem;color:rgba(255,255,255,.85);margin-top:.3rem">
                              {correct_opt}</div></div>""",unsafe_allow_html=True)
                        else:
                            st.markdown(f"""<div style="background:linear-gradient(135deg,#7f0000,#c0392b);
                            border-radius:12px;padding:1.2rem 1.5rem;margin:.8rem 0;color:#fff">
                            <div style="font-size:1.5rem;text-align:center">❌</div>
                            <div style="font-size:.95rem;font-weight:700;color:#fff;margin:.4rem 0">You chose: {user_opt}</div>
                            <div style="font-size:.9rem;color:rgba(255,255,255,.9)">Correct: <strong>{correct_opt}</strong></div>
                            </div>""",unsafe_allow_html=True)

                    # ── Built-in explanation (always available) ─────────────
                    if sel_q.get("explanation"):
                        st.markdown(f"""<div style="background:#e8f5e9;border-radius:12px;
                        padding:1.2rem 1.5rem;border-left:5px solid #27ae60;margin:.8rem 0">
                        <div style="font-size:.75rem;font-weight:700;color:#1b5e20;text-transform:uppercase;
                          letter-spacing:.6px;margin-bottom:.5rem">📖 Expert Explanation</div>
                        <div style="font-size:.92rem;color:#1c2c1e;line-height:1.7">{sel_q["explanation"]}</div>
                        </div>""",unsafe_allow_html=True)

                    if sel_q.get("hint"):
                        st.markdown(f"""<div style="background:#fff8e1;border-radius:10px;
                        padding:.9rem 1.2rem;border-left:4px solid #f39c12;margin:.6rem 0">
                        <div style="font-size:.73rem;font-weight:700;color:#8a6200;text-transform:uppercase;
                          letter-spacing:.5px;margin-bottom:.3rem">💡 Memory Hint</div>
                        <div style="font-size:.88rem;color:#5a4000;line-height:1.55">{sel_q["hint"]}</div>
                        </div>""",unsafe_allow_html=True)

                    # ── All options explained ────────────────────────────────
                    st.markdown("""<div style="background:#f0f4fb;border-radius:10px;padding:1rem 1.2rem;margin:.8rem 0">
                    <div style="font-size:.75rem;font-weight:700;color:#1a3a6b;text-transform:uppercase;margin-bottom:.6rem">
                      📋 All Options Reviewed</div>""",unsafe_allow_html=True)
                    for opt in sel_q["opts"]:
                        is_a = opt[0] == correct_letter
                        is_u = opt[0] == user_choice
                        icon = "✅" if is_a else ("❌" if is_u and submit_disc else "○")
                        bg   = "#eafaf1" if is_a else ("#fce4ec" if is_u and not is_a and submit_disc else "#ffffff")
                        bc   = "#27ae60" if is_a else ("#e74c3c" if is_u and not is_a and submit_disc else "#dce3ee")
                        st.markdown(f"""<div style="background:{bg};border:1.5px solid {bc};
                        border-radius:8px;padding:7px 12px;margin-bottom:5px;
                        font-size:.88rem;color:#1c1c2e;font-weight:{"700" if is_a else "400"}">{icon} {opt}</div>""",
                        unsafe_allow_html=True)
                    st.markdown("</div>",unsafe_allow_html=True)

                    # ── AI Deep Dive (if API key available) ──────────────────
                    st.markdown("---")
                    if st.session_state.api_key:
                        disc_type = "wrong" if (submit_disc and not is_correct) else "explain"
                        btn_label = "🧠 Get AI Professor Tutorial" if disc_type=="wrong" else "🧠 Get AI Deep Explanation"
                        if st.button(btn_label, type="primary", use_container_width=True,
                                     key=f"ai_deep_{sel_q['id']}_{submit_disc}"):
                            with st.spinner("Professor Claude is preparing your tutorial…"):
                                try:
                                    if disc_type == "wrong":
                                        ai_resp = get_discussion(
                                            st.session_state.api_key,
                                            sel_q["q"],
                                            sel_q["opts"],
                                            correct_opt,
                                            user_opt
                                        )
                                    else:
                                        ai_resp = get_explanation(
                                            st.session_state.api_key,
                                            sel_q["q"],
                                            correct_opt,
                                            sel_q.get("topic",""),
                                            sel_q.get("subtopic","")
                                        )
                                    st.markdown(f"""<div style="background:linear-gradient(135deg,#0d2347,#1a3a6b);
                                    border-radius:14px;padding:1.5rem 1.8rem;margin-top:.8rem">
                                    <div style="font-size:.75rem;font-weight:700;color:#d4a017;text-transform:uppercase;
                                      letter-spacing:.7px;margin-bottom:.7rem">🤖 AI Professor Tutorial</div>
                                    <div style="font-size:.91rem;color:#ffffff;line-height:1.75;white-space:pre-wrap">{ai_resp}</div>
                                    </div>""",unsafe_allow_html=True)
                                except ValueError as ve:
                                    st.error(f"API issue: {str(ve)}")
                                except Exception as e:
                                    st.error(f"Could not get AI tutorial: {str(e)}")
                    else:
                        st.markdown("""<div style="background:#f3e5f5;border-radius:10px;padding:1rem 1.3rem;
                        border-left:4px solid #7b1fa2">
                        <div style="font-weight:700;color:#4a148c;font-size:.88rem">🧠 Want deeper AI tutorials?</div>
                        <div style="font-size:.83rem;color:#4a148c;margin-top:.3rem;line-height:1.6">
                          Add your Anthropic API key in the sidebar to get full professor-style AI tutorials
                          with related questions, mnemonics, and exam strategies for every question.
                        </div></div>""",unsafe_allow_html=True)

                    # ── Related questions ────────────────────────────────────
                    st.markdown("---")
                    st.markdown("### 🔗 Related Questions")
                    related = [q for q in all_questions()
                               if q["id"] != sel_q["id"]
                               and q.get("topic")==sel_q.get("topic")
                               and q.get("subtopic")==sel_q.get("subtopic")][:4]
                    if related:
                        for rq in related:
                            rd = rq.get("difficulty","medium")
                            with st.expander(f"[{rd.upper()}] {rq['q'][:80]}..."):
                                for opt in rq["opts"]:
                                    is_a = opt[0]==rq["ans"]
                                    st.markdown(f"<span style='color:{'#27ae60' if is_a else '#2c2c3e'};font-weight:{'700' if is_a else '400'}'>{'✅ ' if is_a else '   '}{opt}</span>",unsafe_allow_html=True)
                                if rq.get("explanation"):
                                    st.markdown(f"*{rq['explanation']}*")
                    else:
                        st.info("No related questions in same subtopic yet. Try generating more!")

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 4: Matrix
    # ══════════════════════════════════════════════════════════════════════════
    with tab4:
        st.markdown("### 📊 Question Bank Matrix")
        aq = all_questions()
        rows = ["| Topic | Easy | Medium | Hard | Total | Pre-loaded | API Gen |",
                "|:---|:---:|:---:|:---:|:---:|:---:|:---:|"]
        for t in TOPICS:
            e   = len([q for q in aq if q["topic"]==t and q["difficulty"]=="easy"])
            m   = len([q for q in aq if q["topic"]==t and q["difficulty"]=="medium"])
            h   = len([q for q in aq if q["topic"]==t and q["difficulty"]=="hard"])
            pre = len([q for q in PRELOADED_QUESTIONS if q["topic"]==t])
            api = len([q for q in st.session_state.ai_questions if q.get("topic")==t])
            rows.append(f"| {t} | {e} | {m} | {h} | **{e+m+h}** | {pre} | {api} |")
        st.markdown("\n".join(rows))

        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📝 Practice All Pre-loaded",type="primary",use_container_width=True):
                pool = PRELOADED_QUESTIONS.copy(); random.shuffle(pool)
                st.session_state.quiz_questions = pool[:min(30,len(pool))]
                st.session_state.current_idx=0; st.session_state.answers={}
                st.session_state.quiz_started=True; st.session_state.quiz_finished=False
                st.session_state.score=0; st.session_state.streak=0
                st.session_state.page="quiz"; st.rerun()
        with c2:
            if st.button("🎯 Hard Questions Only",use_container_width=True):
                pool = [q for q in all_questions() if q["difficulty"]=="hard"]
                random.shuffle(pool)
                st.session_state.quiz_questions = pool[:20]
                st.session_state.current_idx=0; st.session_state.answers={}
                st.session_state.quiz_started=True; st.session_state.quiz_finished=False
                st.session_state.score=0; st.session_state.streak=0
                st.session_state.page="quiz"; st.rerun()
        with c3:
            if st.button("🗑️ Clear API Questions",use_container_width=True):
                st.session_state.ai_questions=[]; st.success("API questions cleared."); st.rerun()



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
