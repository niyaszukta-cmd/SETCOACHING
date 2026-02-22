"""
Kerala SET English Literature & Linguistics — Practice App
Single-file build for Streamlit Cloud compatibility
Author: NYZTrade Education Platform
"""

import streamlit as st
import anthropic
import json
import random
import re

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Kerala SET Practice | NYZTrade",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
:root {
  --primary:#1a3a6b; --secondary:#c0392b; --accent:#2980b9;
  --gold:#d4a017; --success:#27ae60; --fail:#e74c3c;
  --bg:#f4f6fb; --card:#ffffff; --text:#1c1c2e;
  --muted:#6c7a8d; --border:#dce3ee; --r:12px;
  --shadow:0 4px 24px rgba(26,58,107,.10);
}
#MainMenu,footer,header{visibility:hidden}
.block-container{padding-top:1rem;padding-bottom:2rem;max-width:980px}
html,body,[class*="css"]{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text)}

.app-header{background:linear-gradient(135deg,var(--primary) 0%,#0d2347 100%);color:white;
  padding:1.3rem 2rem;border-radius:16px;margin-bottom:1.4rem;
  display:flex;align-items:center;justify-content:space-between;
  box-shadow:0 6px 30px rgba(26,58,107,.25)}
.app-header h1{font-family:'Playfair Display',serif;font-size:1.75rem;margin:0}
.app-header .sub{font-size:.82rem;opacity:.72;margin-top:2px}
.app-header .badge{background:var(--gold);color:#1c1c2e;font-weight:700;
  font-size:.72rem;padding:4px 10px;border-radius:20px;text-transform:uppercase;letter-spacing:.5px}

.stat-row{display:flex;gap:12px;margin-bottom:1.4rem;flex-wrap:wrap}
.sc{background:var(--card);border-radius:var(--r);padding:1rem 1.2rem;flex:1 1 130px;
  box-shadow:var(--shadow);border-left:4px solid var(--primary);min-width:110px}
.sc.gold{border-left-color:var(--gold)} .sc.green{border-left-color:var(--success)}
.sc.red{border-left-color:var(--secondary)}
.sc .lbl{font-size:.7rem;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;font-weight:600}
.sc .val{font-size:1.85rem;font-weight:700;color:var(--primary);line-height:1.1;margin-top:2px}
.sc.gold .val{color:#b8860b} .sc.green .val{color:var(--success)} .sc.red .val{color:var(--secondary)}

.qcard{background:var(--card);border-radius:16px;padding:1.8rem 2rem;
  box-shadow:var(--shadow);border:1px solid var(--border);margin-bottom:1rem}
.qnum{font-size:.72rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:1px;margin-bottom:.5rem}
.qtags{display:flex;gap:6px;margin-bottom:.75rem;flex-wrap:wrap}
.tag{background:#e8eef7;color:var(--primary);font-size:.68rem;font-weight:600;
  padding:2px 9px;border-radius:20px;text-transform:uppercase;letter-spacing:.4px}
.tag.ai{background:#fff3e0;color:#e65100} .tag.hard{background:#fce4ec;color:#c62828}
.tag.easy{background:#e8f5e9;color:#2e7d32} .tag.medium{background:#e3f2fd;color:#1565c0}
.qtext{font-size:1.02rem;font-weight:500;color:var(--text);line-height:1.65;
  margin-bottom:1.3rem;white-space:pre-wrap}

.opt{display:block;width:100%;text-align:left;padding:.7rem 1rem;margin-bottom:.55rem;
  border-radius:10px;border:2px solid var(--border);background:var(--bg);
  font-size:.93rem;color:var(--text)}
.opt.correct{border-color:var(--success);background:#eafaf1;color:#1d6a3a;font-weight:600}
.opt.wrong{border-color:var(--fail);background:#fdf2f2;color:#992222}
.opt.reveal{border-color:var(--success);background:#eafaf1;color:#1d6a3a;font-weight:600}

.pw{background:var(--border);border-radius:20px;height:8px;margin-bottom:1rem;overflow:hidden}
.pb{height:100%;border-radius:20px;background:linear-gradient(90deg,var(--primary),var(--accent));transition:width .4s}

.rcard{background:linear-gradient(135deg,var(--primary),#0d2347);color:white;
  border-radius:20px;padding:2.5rem 2rem;text-align:center;margin:1rem 0;
  box-shadow:0 10px 40px rgba(26,58,107,.3)}
.rscore{font-size:3.8rem;font-weight:800;letter-spacing:-2px}
.rtotal{font-size:1rem;opacity:.7;margin-top:-4px}
.rgrade{font-size:1.35rem;font-weight:600;margin-top:.9rem}

.ai-box{background:linear-gradient(135deg,#1a1a2e,#16213e);border-radius:16px;
  padding:1.6rem;color:white;margin-bottom:1rem}
.ai-box h3{font-family:'Playfair Display',serif;font-size:1.25rem;margin-bottom:.35rem}
.ai-box p{opacity:.70;font-size:.86rem;margin:0}

.streak{display:inline-flex;align-items:center;gap:5px;background:#fff3e0;
  color:#e65100;font-weight:700;font-size:.83rem;padding:4px 13px;border-radius:20px}

[data-testid="stSidebar"]{background:linear-gradient(180deg,#1a3a6b,#0d2347) !important}
[data-testid="stSidebar"] *{color:white !important}
[data-testid="stSidebar"] .stButton>button{
  width:100%;background:rgba(255,255,255,.10) !important;color:white !important;
  border:1px solid rgba(255,255,255,.22) !important;border-radius:8px;margin-bottom:3px}
[data-testid="stSidebar"] .stButton>button:hover{background:rgba(255,255,255,.20) !important}

.stButton>button[kind="primary"]{
  background:linear-gradient(135deg,var(--primary),var(--accent)) !important;
  color:white !important;border:none !important;border-radius:10px !important;
  font-weight:600 !important;box-shadow:0 4px 15px rgba(26,58,107,.25) !important}
hr{border:none;border-top:1px solid var(--border);margin:1.1rem 0}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# QUESTION BANK  (60 curated seed questions)
# ══════════════════════════════════════════════════════════════════════════════
QUESTION_BANK = [
    {"id":1,"topic":"World Literature","subtopic":"African Literature","q":"The novel Things Fall Apart was written by:","opts":["A) Wole Soyinka","B) Chinua Achebe","C) Ngugi wa Thiong'o","D) Ben Okri"],"ans":"B","difficulty":"easy"},
    {"id":2,"topic":"British Literature","subtopic":"Old English","q":"The Old English epic Beowulf is composed in:","opts":["A) Rhyming couplets","B) Alliterative verse","C) Blank verse","D) Terza rima"],"ans":"B","difficulty":"medium"},
    {"id":3,"topic":"British Literature","subtopic":"Modernism","q":"Identify the true statements about Virginia Woolf:\nStatement 1: She was a member of the Bloomsbury Group.\nStatement 2: She founded the Hogarth Press.","opts":["A) 1 only","B) 2 only","C) Both 1 & 2","D) Neither 1 nor 2"],"ans":"C","difficulty":"easy"},
    {"id":4,"topic":"British Literature","subtopic":"Romanticism","q":"\"Because I could not stop for Death\" was written by:","opts":["A) Christina Rossetti","B) Emily Brontë","C) Emily Dickinson","D) Sylvia Plath"],"ans":"C","difficulty":"easy"},
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
    {"id":21,"topic":"Literary Theory","subtopic":"Criticism","q":"The Great Tradition (1948), evaluating the English novel, was written by:","opts":["A) I.A. Richards","B) F.R. Leavis","C) William Empson","D) Raymond Williams"],"ans":"B","difficulty":"medium"},
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
    {"id":37,"topic":"Indian Literature","subtopic":"Drama","q":"Tale Danda (Taledanda) by Girish Karnad dramatises conflict between:","opts":["A) Mughal court factions","B) Brahminical orthodoxy and Veerashaiva reform","C) Hindu and Muslim communities","D) Colonial rulers and nationalists"],"ans":"B","difficulty":"medium"},
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
]

TOPICS = sorted(set(q["topic"] for q in QUESTION_BANK))
DIFFICULTIES = ["easy", "medium", "hard"]

AI_TOPIC_PROMPTS = {
    "British Literature": "Old English (Beowulf), Medieval (Chaucer, Langland, Pearl-Poet), Renaissance (Shakespeare, Spenser, Marlowe, Sidney, Milton, Jonson, Donne), Restoration (Dryden, Congreve), 18th Century (Pope, Swift, Johnson, Goldsmith, Richardson, Fielding, Sterne), Romanticism (Blake, Wordsworth, Coleridge, Keats, Shelley, Byron, Lamb, Hazlitt, De Quincey), Victorian (Dickens, Hardy, Eliot, Tennyson, Browning, Arnold, Ruskin, Pater, Rossetti, Swinburne), Modernism (Woolf, Joyce, Eliot, Lawrence, Forster, Yeats, Auden, Beckett, Pound), 20th-century drama (Pinter, Osborne, Stoppard), Contemporary British fiction",
    "American Literature": "Transcendentalism (Emerson, Thoreau, Whitman), 19th-century fiction (Hawthorne, Melville, Poe, Twain, Henry James), Emily Dickinson, Realism (Chopin, Crane), Modernism (Hemingway, Fitzgerald, Faulkner, Steinbeck), Poetry (Frost, Stevens, Williams, Moore, Bishop, Plath, Lowell), Harlem Renaissance (Hughes, Hurston, Toomer), Drama (O'Neill, Miller, Tennessee Williams), Postwar fiction (Toni Morrison, Alice Walker, Pynchon)",
    "Indian Literature": "Indian Writing in English (Raja Rao, Mulk Raj Anand, R.K. Narayan, Rushdie, Arundhati Roy, Vikram Seth, Amitav Ghosh, Kiran Desai, Rohinton Mistry), Indian drama (Girish Karnad, Vijay Tendulkar, Mahesh Dattani, Badal Sircar, Mohan Rakesh), Indian poets in English (Ezekiel, Ramanujan, Daruwalla, Kamala Das, Dom Moraes, Tagore, Sarojini Naidu, Toru Dutt)",
    "World Literature": "African (Achebe, Soyinka, Ngugi, Adichie, Dangarembga, Okri), Caribbean (Walcott, Rhys, Naipaul, Lamming), Canadian (Atwood, Munro, Ondaatje, Laurence), Australian (Patrick White, Les Murray, David Malouf), Postcolonial fiction globally, Nobel laureates in Literature",
    "Literary Theory": "Classical (Aristotle Poetics, Horace Ars Poetica), Renaissance (Sidney's Defence of Poesy), Neoclassical (Dryden, Pope, Johnson), Romantic criticism (Wordsworth Preface, Coleridge Biographia Literaria), Victorian (Arnold Culture and Anarchy, Pater Renaissance), New Criticism (I.A. Richards, Empson, Brooks, Ransom, Wimsatt), Russian Formalism (Shklovsky, Jakobson), Structuralism (Saussure, Lévi-Strauss, Barthes), Post-structuralism and Deconstruction (Derrida, de Man, Lacan), Marxism (Althusser, Gramsci, Williams, Eagleton, Jameson), Feminism (Showalter, Cixous, Kristeva, Irigaray, Butler), Postcolonialism (Said, Bhabha, Spivak, Fanon), New Historicism (Greenblatt), Narratology (Genette), Reader-Response (Iser, Fish, Jauss)",
    "Linguistics": "Phonetics (IPA, place and manner of articulation), Phonology (phonemes, allophones, syllable structure), Morphology (affixation, compounding, conversion, blending, clipping), Syntax (phrase structure, transformational grammar), Semantics (sense relations, semantic change, amelioration, pejoration), Pragmatics (speech acts, Grice's maxims, implicature), Historical linguistics (Great Vowel Shift, Grimm's Law, Indo-European family tree), Sociolinguistics (register, dialect, code-switching, pidgin and creole), Language acquisition (Chomsky LAD, Skinner behaviourism, Piaget, Vygotsky), Language teaching methods (Grammar-Translation, Direct Method, Audio-Lingual, CLT, Task-Based)",
}

SUBTOPIC_MAP = {
    "British Literature": ["Old English","Medieval","Renaissance","Restoration","18th Century","Romanticism","Victorian","Modernism","20th Century Drama","Contemporary"],
    "American Literature": ["Colonial","Transcendentalism","19th Century Fiction","Poetry","Modernism","Harlem Renaissance","Drama","Contemporary"],
    "Indian Literature": ["Fiction","Poetry","Drama","Partition Literature","Dalit Literature","Postcolonial Fiction"],
    "World Literature": ["African Literature","Caribbean Literature","Australian Literature","Canadian Literature","Nobel Laureates"],
    "Literary Theory": ["Classical","New Criticism","Structuralism","Poststructuralism","Deconstruction","Feminism","Marxism","Postcolonialism","New Historicism","Psychoanalytic Criticism"],
    "Linguistics": ["Phonetics","Phonology","Morphology","Syntax","Semantics","Pragmatics","Language Acquisition","Sociolinguistics","Language Teaching","Historical Linguistics"],
}

QUESTION_TYPES = [
    "identification (who wrote / who said / which work contains)",
    "definition of a literary or linguistic term",
    "chronological ordering of works or literary periods",
    "true/false statement pairs (Statement 1 / Statement 2 format)",
    "match List I with List II (4 items each side)",
    "complete the famous quote (fill the blank)",
    "multiple works by same author (identify which belong to whom)",
    "which literary period or movement does this belong to",
    "character identification (who says / appears in which work)",
    "identify the correct or incorrect statement about a critical concept",
]

ANGLES = [
    "focusing on dates and first publication facts",
    "about key quotations and their sources",
    "from a literary history and periodisation angle",
    "about critical reception and famous critics' views",
    "about influence, intertextuality, and literary debts",
    "about narrative technique, point of view, or form",
    "about thematic concerns, symbols, and imagery",
    "about the author's biography and historical context",
    "about genre classifications and formal features",
    "about theoretical frameworks and schools of thought",
]


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
def init_state():
    defaults = {
        "api_key": "", "ai_questions": [], "quiz_questions": [],
        "current_idx": 0, "answers": {}, "quiz_started": False,
        "quiz_finished": False, "score": 0, "page": "home",
        "total_attempted": 0, "total_correct": 0,
        "topic_stats": {}, "difficulty_stats": {},
        "streak": 0, "best_streak": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def all_questions():
    return QUESTION_BANK + st.session_state.ai_questions

def start_quiz(topic_filter=None, difficulty_filter=None, count=20):
    pool = all_questions()
    if topic_filter:
        pool = [q for q in pool if q["topic"] in topic_filter]
    if difficulty_filter:
        pool = [q for q in pool if q["difficulty"] in difficulty_filter]
    random.shuffle(pool)
    st.session_state.quiz_questions = pool[:count]
    st.session_state.current_idx = 0
    st.session_state.answers = {}
    st.session_state.quiz_started = True
    st.session_state.quiz_finished = False
    st.session_state.score = 0
    st.session_state.streak = 0

def submit_answer(q_id, letter):
    q = next((x for x in st.session_state.quiz_questions if x["id"] == q_id), None)
    if q is None or q_id in st.session_state.answers:
        return None
    correct = q["ans"]
    ok = letter == correct
    st.session_state.answers[q_id] = {"selected": letter, "correct": correct, "is_correct": ok}
    st.session_state.total_attempted += 1
    t = q.get("topic","Other"); d = q.get("difficulty","medium")
    for store, key in [(st.session_state.topic_stats, t), (st.session_state.difficulty_stats, d)]:
        if key not in store: store[key] = {"attempted":0,"correct":0}
        store[key]["attempted"] += 1
    if ok:
        st.session_state.total_correct += 1
        st.session_state.score += 1
        st.session_state.streak += 1
        st.session_state.topic_stats[t]["correct"] += 1
        st.session_state.difficulty_stats[d]["correct"] += 1
        if st.session_state.streak > st.session_state.best_streak:
            st.session_state.best_streak = st.session_state.streak
    else:
        st.session_state.streak = 0
    return ok

def reset_quiz():
    st.session_state.quiz_started = False
    st.session_state.quiz_finished = False
    st.session_state.answers = {}
    st.session_state.quiz_questions = []
    st.session_state.current_idx = 0
    st.session_state.score = 0
    st.session_state.streak = 0


# ══════════════════════════════════════════════════════════════════════════════
# AI GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
def generate_questions_ai(api_key, topic, subtopic, difficulty, count=5, existing=None):
    if not existing: existing = []
    q_type = random.choice(QUESTION_TYPES)
    angle  = random.choice(ANGLES)
    context = AI_TOPIC_PROMPTS.get(topic, topic)
    existing_sample = "\n".join(f"- {q}" for q in existing[:8])

    prompt = f"""You are an expert question setter for the Kerala SET exam in English Language and Literature.

Generate exactly {count} original MCQ questions.

SPECIFICATIONS:
- Topic: {topic}  |  Subtopic: {subtopic}  |  Difficulty: {difficulty}
- Question type style: {q_type}
- Approach angle: {angle}
- Syllabus context: {context}

RULES:
1. Exactly 4 options: A) B) C) D)
2. One correct answer only
3. Plausible but clearly wrong distractors
4. Do NOT repeat these existing questions:
{existing_sample if existing_sample else "(none)"}
5. University-level English literature/linguistics standard

Respond with ONLY valid JSON, no markdown:
{{"questions":[{{"q":"...","opts":["A) ...","B) ...","C) ...","D) ..."],"ans":"A","topic":"{topic}","subtopic":"{subtopic}","difficulty":"{difficulty}"}}]}}"""

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-opus-4-6", max_tokens=4096,
        messages=[{"role":"user","content":prompt}]
    )
    raw = response.content[0].text.strip()
    m = re.search(r'\{.*\}', raw, re.DOTALL)
    if not m: return []
    data = json.loads(m.group())
    questions = data.get("questions", [])
    start_id = 10000 + random.randint(100, 89000)
    valid = []
    for i, q in enumerate(questions):
        q["id"] = start_id + i
        q["ai_generated"] = True
        if all(k in q for k in ["q","opts","ans"]) and len(q["opts"])==4 and q["ans"] in "ABCD":
            valid.append(q)
    return valid

def generate_batch(api_key, topics, difficulties, total_count, existing=None, progress_cb=None):
    if not existing: existing = []
    combos = [(t, d) for t in topics for d in difficulties]
    random.shuffle(combos)
    per = max(1, total_count // len(combos)) if combos else 1
    rem = total_count - per * len(combos)
    all_new = []
    for idx, (topic, diff) in enumerate(combos):
        n = per + (1 if idx < rem else 0)
        if n <= 0: continue
        subtopic = random.choice(SUBTOPIC_MAP.get(topic, [topic]))
        try:
            new_qs = generate_questions_ai(api_key, topic, subtopic, diff, count=n, existing=existing)
            all_new.extend(new_qs)
            existing.extend([q["q"] for q in new_qs])
        except Exception:
            pass
        if progress_cb: progress_cb(idx+1, len(combos))
    return all_new


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 📚 Kerala SET")
    st.markdown("### English Literature 2026")
    st.markdown("---")

    nav_items = [
        ("🏠 Home", "home"),
        ("📝 Practice Quiz", "quiz"),
        ("🤖 AI Generator", "ai_gen"),
        ("📊 Analytics", "analytics"),
        ("📖 Question Bank", "bank"),
    ]
    for label, key in nav_items:
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            if key != "quiz":
                reset_quiz()
            st.rerun()

    st.markdown("---")
    st.markdown("##### 🔑 Anthropic API Key")
    api_input = st.text_input("API Key", value=st.session_state.api_key,
        type="password", label_visibility="collapsed", placeholder="sk-ant-...")
    if api_input != st.session_state.api_key:
        st.session_state.api_key = api_input

    total_q = len(QUESTION_BANK) + len(st.session_state.ai_questions)
    ai_q    = len(st.session_state.ai_questions)
    if st.session_state.api_key:
        st.markdown(f"<small>✅ Key set · 🗂 **{total_q}** questions ({ai_q} AI)</small>", unsafe_allow_html=True)
    else:
        st.markdown("<small style='opacity:.6'>Enter key to unlock AI generation</small>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<small style='opacity:.5'>NYZTrade Education · Kerala SET 2026</small>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: HOME
# ══════════════════════════════════════════════════════════════════════════════
def page_home():
    st.markdown("""
    <div class="app-header">
      <div><h1>📚 Kerala SET Practice</h1>
      <div class="sub">English Language & Literature · AI-Powered Q&A System</div></div>
      <div class="badge">SET 2026</div>
    </div>""", unsafe_allow_html=True)

    ai_c = len(st.session_state.ai_questions)
    tot  = len(QUESTION_BANK) + ai_c
    att  = st.session_state.total_attempted
    cor  = st.session_state.total_correct
    acc  = round(cor/att*100) if att else 0
    bst  = st.session_state.best_streak

    st.markdown(f"""
    <div class="stat-row">
      <div class="sc"><div class="lbl">Total Questions</div><div class="val">{tot}</div></div>
      <div class="sc green"><div class="lbl">Attempted</div><div class="val">{att}</div></div>
      <div class="sc gold"><div class="lbl">Accuracy</div><div class="val">{acc}%</div></div>
      <div class="sc red"><div class="lbl">Best Streak 🔥</div><div class="val">{bst}</div></div>
      <div class="sc"><div class="lbl">AI Generated</div><div class="val">{ai_c}</div></div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### 🚀 Quick Start")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("⚡ Quick 10 Qs", use_container_width=True, type="primary"):
                start_quiz(count=10); st.session_state.page = "quiz"; st.rerun()
        with c2:
            if st.button("📝 Mock Test (50)", use_container_width=True):
                start_quiz(count=50); st.session_state.page = "quiz"; st.rerun()
        with c3:
            if st.button("🎯 Hard Mode (20)", use_container_width=True):
                start_quiz(difficulty_filter=["hard"], count=20); st.session_state.page = "quiz"; st.rerun()

        st.markdown("### 📋 Topic Coverage")
        ts = st.session_state.topic_stats
        for topic in TOPICS:
            pool = [q for q in all_questions() if q["topic"]==topic]
            att_t = ts.get(topic,{}).get("attempted",0)
            cor_t = ts.get(topic,{}).get("correct",0)
            acc_t = round(cor_t/att_t*100) if att_t else 0
            pct   = round(att_t/len(pool)*100) if pool else 0
            st.markdown(f"""
            <div style="margin-bottom:9px">
              <div style="display:flex;justify-content:space-between;font-size:.83rem;margin-bottom:3px">
                <span style="font-weight:500">{topic}</span>
                <span style="color:#6c7a8d">{len(pool)} Qs · {att_t} done · {acc_t}% acc</span>
              </div>
              <div class="pw"><div class="pb" style="width:{pct}%"></div></div>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("### 🎯 Practice by Topic")
        for topic in TOPICS:
            if st.button(f"📌 {topic}", key=f"ht_{topic}", use_container_width=True):
                start_quiz(topic_filter=[topic], count=15)
                st.session_state.page = "quiz"; st.rerun()
        st.markdown("---")
        st.markdown("### 💡 How it works")
        st.markdown("""
1. **60 Seed Questions** – expertly curated  
2. **AI Multiply** – Claude generates 100s more  
3. **Filter** by topic & difficulty  
4. **Track** your live performance  
5. **Analyse** weak areas in Analytics
        """)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: QUIZ
# ══════════════════════════════════════════════════════════════════════════════
def page_quiz():
    st.markdown("""
    <div class="app-header">
      <div><h1>📝 Practice Quiz</h1>
      <div class="sub">Test your Kerala SET preparation</div></div>
    </div>""", unsafe_allow_html=True)

    # Setup panel
    if not st.session_state.quiz_started:
        st.markdown("### ⚙️ Configure Your Quiz")
        col1, col2 = st.columns(2)
        with col1:
            topics_sel = st.multiselect("Topics (empty = all)", TOPICS, key="qs_t")
            diff_sel   = st.multiselect("Difficulties (empty = all)", DIFFICULTIES, default=DIFFICULTIES, key="qs_d")
        with col2:
            pool_size = len([q for q in all_questions()
                             if (not topics_sel or q["topic"] in topics_sel)
                             and (not diff_sel or q["difficulty"] in diff_sel)])
            count = st.slider("Number of Questions", 5, min(pool_size, 120), 20, key="qs_n")
            st.info(f"📦 **{pool_size}** questions match your filters")
        st.markdown("---")
        if st.button("🚀 Start Quiz", type="primary", use_container_width=True):
            if pool_size == 0:
                st.error("No questions match — try broadening filters.")
            else:
                start_quiz(topic_filter=topics_sel or None, difficulty_filter=diff_sel or None, count=count)
                st.rerun()
        return

    questions = st.session_state.quiz_questions
    if not questions:
        st.warning("No questions loaded."); reset_quiz(); st.rerun(); return

    total    = len(questions)
    answered = len(st.session_state.answers)

    if st.session_state.quiz_finished or answered >= total:
        _results(questions); return

    idx = st.session_state.current_idx
    if idx >= total:
        st.session_state.quiz_finished = True; st.rerun()

    q = questions[idx]
    already = q["id"] in st.session_state.answers

    pct = int(answered/total*100)
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;font-size:.8rem;color:#6c7a8d;margin-bottom:4px">
      <span>Question {idx+1} of {total}</span>
      <span>✅ {st.session_state.score} correct · streak 🔥{st.session_state.streak}</span>
    </div>
    <div class="pw"><div class="pb" style="width:{pct}%"></div></div>""", unsafe_allow_html=True)

    dc = q.get("difficulty","medium")
    ai_tag = '<span class="tag ai">🤖 AI</span>' if q.get("ai_generated") else ""
    st.markdown(f"""
    <div class="qcard">
      <div class="qnum">Question {idx+1}</div>
      <div class="qtags">
        <span class="tag">{q.get("topic","")}</span>
        <span class="tag">{q.get("subtopic","")}</span>
        <span class="tag {dc}">{dc.upper()}</span>{ai_tag}
      </div>
      <div class="qtext">{q["q"]}</div>
    </div>""", unsafe_allow_html=True)

    correct_letter = q["ans"]
    user_ans = st.session_state.answers.get(q["id"])

    for opt in q["opts"]:
        letter = opt[0]
        if already:
            if letter == correct_letter:     cls = "opt correct"
            elif user_ans and letter == user_ans["selected"]: cls = "opt wrong"
            else:                             cls = "opt"
            st.markdown(f'<div class="{cls}">{opt}</div>', unsafe_allow_html=True)
        else:
            if st.button(opt, key=f"o_{q['id']}_{letter}", use_container_width=True):
                submit_answer(q["id"], letter); st.rerun()

    if already:
        correct_opt = next(o for o in q["opts"] if o[0] == correct_letter)
        if user_ans["is_correct"]:
            st.success(f"✅ Correct! **{correct_opt}**")
        else:
            sel_opt = next((o for o in q["opts"] if o[0] == user_ans["selected"]), "")
            st.error(f"❌ You chose **{sel_opt}** · Correct: **{correct_opt}**")

        _, mid, _ = st.columns([1,2,1])
        with mid:
            lbl = "Next ➡️" if idx < total-1 else "Finish 🏁"
            if st.button(lbl, type="primary", use_container_width=True, key="next_btn"):
                if idx < total-1:
                    st.session_state.current_idx += 1; st.rerun()
                else:
                    st.session_state.quiz_finished = True; st.rerun()

    st.markdown("---")
    if st.button("🔄 Restart", key="restart"): reset_quiz(); st.rerun()


def _results(questions):
    total = len(questions); score = st.session_state.score
    pct   = round(score/total*100) if total else 0
    grade = ("Excellent! 🏆" if pct>=80 else "Good 👍" if pct>=60
             else "Needs Improvement 📖" if pct>=40 else "Keep Studying 💪")

    st.markdown(f"""
    <div class="rcard">
      <div class="rscore">{score}/{total}</div>
      <div class="rtotal">Questions Correct</div>
      <div class="rgrade">{grade} — {pct}%</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("### 📊 Topic Breakdown")
    tr = {}
    for q in questions:
        t = q.get("topic","Other")
        if t not in tr: tr[t] = {"a":0,"c":0}
        if q["id"] in st.session_state.answers:
            tr[t]["a"] += 1
            if st.session_state.answers[q["id"]]["is_correct"]: tr[t]["c"] += 1
    for topic, s in tr.items():
        acc = round(s["c"]/s["a"]*100) if s["a"] else 0
        col = "#27ae60" if acc>=70 else "#e67e22" if acc>=50 else "#e74c3c"
        st.markdown(f"""
        <div style="margin-bottom:9px">
          <div style="display:flex;justify-content:space-between;font-size:.83rem;margin-bottom:3px">
            <span style="font-weight:500">{topic}</span>
            <span style="color:#6c7a8d">{s['c']}/{s['a']} ({acc}%)</span>
          </div>
          <div class="pw"><div class="pb" style="width:{acc}%;background:{col}"></div></div>
        </div>""", unsafe_allow_html=True)

    wrong = [q for q in questions if q["id"] in st.session_state.answers
             and not st.session_state.answers[q["id"]]["is_correct"]]
    if wrong:
        with st.expander(f"📋 Review {len(wrong)} Wrong Answers"):
            for q in wrong:
                res = st.session_state.answers[q["id"]]
                co  = next(o for o in q["opts"] if o[0]==q["ans"])
                yo  = next((o for o in q["opts"] if o[0]==res["selected"]), "–")
                st.markdown(f"""
                <div style="background:#fff8f8;border-left:3px solid #e74c3c;border-radius:6px;
                  padding:10px 14px;margin-bottom:9px">
                  <div style="font-weight:500;margin-bottom:5px">{q["q"]}</div>
                  <div style="font-size:.83rem;color:#e74c3c">❌ You: {yo}</div>
                  <div style="font-size:.83rem;color:#27ae60">✅ Correct: {co}</div>
                </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔄 New Quiz", type="primary", use_container_width=True): reset_quiz(); st.rerun()
    with c2:
        if st.button("🏠 Home", use_container_width=True):
            reset_quiz(); st.session_state.page = "home"; st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: AI GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
def page_ai_gen():
    st.markdown("""
    <div class="app-header">
      <div><h1>🤖 AI Question Generator</h1>
      <div class="sub">Multiply your practice set using Claude AI</div></div>
      <div class="badge">Powered by Claude</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="ai-box">
      <h3>⚡ Permutation & Combination Engine</h3>
      <p>Selects every combination of Topic × Difficulty × Question Type × Angle, then prompts Claude 
      to generate unique questions for each combo — multiplying your bank from 60 to 500+ instantly.</p>
    </div>""", unsafe_allow_html=True)

    if not st.session_state.api_key:
        st.warning("🔑 Please enter your Anthropic API key in the sidebar to use AI generation.")
        st.info("Get your free API key at: https://console.anthropic.com")
        return

    ai_c = len(st.session_state.ai_questions)
    c1,c2,c3 = st.columns(3)
    c1.metric("Seed Questions", len(QUESTION_BANK))
    c2.metric("AI Generated", ai_c)
    c3.metric("Total", len(QUESTION_BANK)+ai_c, delta=f"+{ai_c} AI" if ai_c else None)

    st.markdown("---")
    st.markdown("### 🎛️ Generation Settings")
    col1, col2 = st.columns(2)
    with col1:
        sel_topics = st.multiselect("Topics", TOPICS, default=TOPICS, key="gen_t")
        sel_diffs  = st.multiselect("Difficulties", DIFFICULTIES, default=DIFFICULTIES, key="gen_d")
    with col2:
        n_q = st.slider("Total to generate", 10, 200, 30, step=10, key="gen_n")
        combos = len(sel_topics) * len(sel_diffs)
        if combos:
            per = max(1, n_q // combos)
            st.info(f"📐 **{combos}** combos → ~**{per}** each → ~**{combos*per}** total")

    st.markdown("---")
    if st.button("🚀 Generate with AI", type="primary", use_container_width=True):
        if not sel_topics or not sel_diffs:
            st.error("Select at least one topic and one difficulty.")
        else:
            existing = [q["q"] for q in QUESTION_BANK + st.session_state.ai_questions]
            bar  = st.progress(0)
            stat = st.empty()
            err  = st.empty()
            def cb(done, total_c):
                bar.progress(int(done/total_c*100))
                stat.markdown(f"⏳ Generating… combo **{done}/{total_c}**")
            try:
                new_qs = generate_batch(st.session_state.api_key, sel_topics, sel_diffs,
                                        n_q, existing=existing, progress_cb=cb)
                st.session_state.ai_questions.extend(new_qs)
                bar.progress(100); stat.empty()
                st.success(f"✅ Generated **{len(new_qs)}** new questions! Total: **{len(QUESTION_BANK)+len(st.session_state.ai_questions)}**")
                st.balloons()
            except anthropic.AuthenticationError:
                bar.empty(); stat.empty()
                err.error("❌ Invalid API key. Please check your key in the sidebar.")
            except anthropic.RateLimitError:
                bar.empty(); stat.empty()
                err.error("❌ Rate limit hit. Please wait a moment and try again.")
            except Exception as e:
                bar.empty(); stat.empty()
                err.error(f"❌ Error: {str(e)}")

    # Preview
    if st.session_state.ai_questions:
        st.markdown("---")
        st.markdown(f"### 📋 AI Questions Preview ({len(st.session_state.ai_questions)} total)")
        pf1,pf2 = st.columns(2)
        with pf1: f_t = st.selectbox("Filter topic", ["All"]+TOPICS, key="pf_t")
        with pf2: f_d = st.selectbox("Filter difficulty", ["All"]+DIFFICULTIES, key="pf_d")
        filtered = st.session_state.ai_questions
        if f_t != "All": filtered = [q for q in filtered if q.get("topic")==f_t]
        if f_d != "All": filtered = [q for q in filtered if q.get("difficulty")==f_d]
        st.markdown(f"Showing **{min(len(filtered),15)}** of **{len(filtered)}**")
        for q in filtered[:15]:
            with st.expander(f"🤖 [{q.get('difficulty','?').upper()}] {q['q'][:85]}..."):
                for opt in q["opts"]:
                    is_a = opt[0]==q["ans"]
                    st.markdown(f"<span style='color:{'#27ae60' if is_a else '#555'};font-weight:{'700' if is_a else '400'}'>{'✅ ' if is_a else '   '}{opt}</span>", unsafe_allow_html=True)

        if st.button("🗑️ Clear AI Questions"):
            st.session_state.ai_questions = []; st.success("Cleared."); st.rerun()

    # Matrix
    st.markdown("---")
    st.markdown("### 🔢 Question Count Matrix")
    aq = QUESTION_BANK + st.session_state.ai_questions
    rows = ["| Topic | Easy | Medium | Hard | Total |", "|---|---|---|---|---|"]
    for t in TOPICS:
        e = len([q for q in aq if q["topic"]==t and q["difficulty"]=="easy"])
        m = len([q for q in aq if q["topic"]==t and q["difficulty"]=="medium"])
        h = len([q for q in aq if q["topic"]==t and q["difficulty"]=="hard"])
        rows.append(f"| {t} | {e} | {m} | {h} | **{e+m+h}** |")
    st.markdown("\n".join(rows))


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
def page_analytics():
    st.markdown("""
    <div class="app-header">
      <div><h1>📊 Performance Analytics</h1>
      <div class="sub">Track your Kerala SET preparation progress</div></div>
    </div>""", unsafe_allow_html=True)

    att = st.session_state.total_attempted
    cor = st.session_state.total_correct
    acc = round(cor/att*100) if att else 0
    bst = st.session_state.best_streak
    ai_c= len(st.session_state.ai_questions)

    st.markdown(f"""
    <div class="stat-row">
      <div class="sc green"><div class="lbl">Attempted</div><div class="val">{att}</div></div>
      <div class="sc gold"><div class="lbl">Correct</div><div class="val">{cor}</div></div>
      <div class="sc"><div class="lbl">Accuracy</div><div class="val">{acc}%</div></div>
      <div class="sc red"><div class="lbl">Best Streak 🔥</div><div class="val">{bst}</div></div>
      <div class="sc"><div class="lbl">AI Questions</div><div class="val">{ai_c}</div></div>
    </div>""", unsafe_allow_html=True)

    if att == 0:
        st.info("🎯 No data yet — take some quizzes first!")
        if st.button("▶️ Start a Quiz", type="primary"):
            start_quiz(count=10); st.session_state.page = "quiz"; st.rerun()
        return

    st.markdown("### 📚 Performance by Topic")
    ts = st.session_state.topic_stats
    for topic in TOPICS:
        s = ts.get(topic, {"attempted":0,"correct":0})
        if s["attempted"]==0: continue
        a = round(s["correct"]/s["attempted"]*100)
        col = "#27ae60" if a>=70 else "#e67e22" if a>=50 else "#e74c3c"
        lbl = "🟢 Strong" if a>=70 else "🟡 Moderate" if a>=50 else "🔴 Needs Work"
        st.markdown(f"""
        <div style="background:white;border-radius:10px;padding:13px 16px;margin-bottom:7px;
          box-shadow:0 2px 8px rgba(0,0,0,.06);display:flex;align-items:center;gap:12px">
          <div style="flex:1">
            <div style="font-weight:600;font-size:.93rem">{topic}</div>
            <div style="font-size:.76rem;color:#6c7a8d;margin-top:2px">{s['correct']}/{s['attempted']} correct</div>
          </div>
          <div style="text-align:right;min-width:110px">
            <div style="font-size:1.45rem;font-weight:700;color:{col}">{a}%</div>
            <div style="font-size:.7rem;color:#6c7a8d">{lbl}</div>
          </div>
        </div>
        <div class="pw" style="margin-top:-4px;margin-bottom:5px"><div class="pb" style="width:{a}%;background:{col}"></div></div>
        """, unsafe_allow_html=True)

    st.markdown("### 🎯 Difficulty Breakdown")
    ds = st.session_state.difficulty_stats
    cols = st.columns(3)
    dc = {"easy":"#27ae60","medium":"#2980b9","hard":"#c0392b"}
    for i, diff in enumerate(DIFFICULTIES):
        s = ds.get(diff,{"attempted":0,"correct":0})
        a = round(s["correct"]/s["attempted"]*100) if s["attempted"] else 0
        with cols[i]:
            st.markdown(f"""
            <div style="background:white;border-radius:12px;padding:18px 14px;text-align:center;
              box-shadow:0 2px 8px rgba(0,0,0,.06);border-top:4px solid {dc[diff]}">
              <div style="font-size:1.9rem;font-weight:800;color:{dc[diff]}">{a}%</div>
              <div style="font-weight:600;margin-top:3px">{diff.capitalize()}</div>
              <div style="font-size:.76rem;color:#6c7a8d;margin-top:3px">{s['correct']}/{s['attempted']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 💡 Study Recommendations")
    weak = [t for t in TOPICS if ts.get(t,{}).get("attempted",0)>0
            and round(ts[t]["correct"]/ts[t]["attempted"]*100)<60]
    unt  = [t for t in TOPICS if ts.get(t,{}).get("attempted",0)==0]
    if weak:
        st.warning(f"**⚠️ Focus Areas:** {', '.join(weak)} — accuracy below 60%")
        if st.button(f"📝 Practice {weak[0]}", type="primary"):
            start_quiz(topic_filter=[weak[0]], count=15)
            st.session_state.page = "quiz"; st.rerun()
    if unt:
        st.info(f"**📌 Not yet attempted:** {', '.join(unt)}")
    if acc>=75: st.success("🏆 Excellent! Focus on Hard difficulty to sharpen further.")
    elif acc>=55: st.info("📈 Good progress! Keep consistent practice across all topics.")
    else: st.warning("📖 Keep going! Build confidence with Easy and Medium questions first.")

    st.markdown("---")
    if st.button("🔄 Reset Statistics"):
        for k in ["total_attempted","total_correct","topic_stats","difficulty_stats","best_streak","streak"]:
            st.session_state[k] = {} if "stats" in k else 0
        st.success("Statistics reset."); st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: QUESTION BANK
# ══════════════════════════════════════════════════════════════════════════════
def page_bank():
    st.markdown("""
    <div class="app-header">
      <div><h1>📖 Question Bank</h1>
      <div class="sub">Browse, filter and explore all questions</div></div>
    </div>""", unsafe_allow_html=True)

    aq   = all_questions()
    seed = [q for q in aq if not q.get("ai_generated")]
    ai_q = [q for q in aq if q.get("ai_generated")]
    c1,c2,c3 = st.columns(3)
    c1.metric("Total", len(aq)); c2.metric("Curated", len(seed)); c3.metric("AI", len(ai_q))

    st.markdown("---")
    col1,col2,col3,col4 = st.columns(4)
    with col1: f_t  = st.selectbox("Topic", ["All"]+TOPICS, key="bk_t")
    with col2: f_d  = st.selectbox("Difficulty", ["All"]+DIFFICULTIES, key="bk_d")
    with col3: f_s  = st.selectbox("Source", ["All","Curated","AI"], key="bk_s")
    with col4: srch = st.text_input("Search", placeholder="keyword…", key="bk_q")

    filtered = aq
    if f_t != "All": filtered = [q for q in filtered if q["topic"]==f_t]
    if f_d != "All": filtered = [q for q in filtered if q["difficulty"]==f_d]
    if f_s == "Curated": filtered = [q for q in filtered if not q.get("ai_generated")]
    elif f_s == "AI":    filtered = [q for q in filtered if q.get("ai_generated")]
    if srch:
        kw = srch.lower()
        filtered = [q for q in filtered if kw in q["q"].lower() or any(kw in o.lower() for o in q["opts"])]

    PAGE_SIZE = 15
    total_p = max(1,(len(filtered)+PAGE_SIZE-1)//PAGE_SIZE)
    pg = st.number_input("Page", 1, total_p, 1, key="bk_pg")
    st.markdown(f"**{len(filtered)}** questions match · Page {pg}/{total_p}")
    page_qs = filtered[(pg-1)*PAGE_SIZE : pg*PAGE_SIZE]

    for q in page_qs:
        dc  = q.get("difficulty","medium")
        pre = "🤖 " if q.get("ai_generated") else ""
        with st.expander(f"{pre}[{q['topic']} · {dc.upper()}] {q['q'][:90]}{'...' if len(q['q'])>90 else ''}"):
            st.markdown(f"**Topic:** {q['topic']} · **Subtopic:** {q.get('subtopic','')} · **Difficulty:** {dc}")
            for opt in q["opts"]:
                is_a = opt[0]==q["ans"]
                st.markdown(f"<span style='color:{'#27ae60' if is_a else '#444'};font-weight:{'700' if is_a else '400'}'>{'✅ ' if is_a else '   '}{opt}</span>", unsafe_allow_html=True)
            if st.button("📝 Practice this topic", key=f"bk_prac_{q['id']}"):
                start_quiz(topic_filter=[q["topic"]], count=10)
                st.session_state.page = "quiz"; st.rerun()

    st.markdown("---")
    if st.button("📥 Export filtered questions as .txt"):
        lines = []
        for i,q in enumerate(filtered,1):
            lines.append(f"Q{i}. {q['q']}")
            for opt in q["opts"]:
                lines.append(f"   {'→ ' if opt[0]==q['ans'] else '  '}{opt}")
            lines.append(f"   Answer: {q['ans']} | {q['topic']} | {q['difficulty']}\n")
        st.download_button("⬇️ Download .txt", "\n".join(lines).encode(),
                           "kerala_set_questions.txt", "text/plain")


# ══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════════
page = st.session_state.page
if   page == "home":      page_home()
elif page == "quiz":      page_quiz()
elif page == "ai_gen":    page_ai_gen()
elif page == "analytics": page_analytics()
elif page == "bank":      page_bank()
else:                     page_home()
