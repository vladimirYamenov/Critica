# backend/api/seed/seed_all_nodes.py
import os, sys, django

sys.path.insert(0, os.path.join(
    os.path.dirname(__file__), '..', '..'))
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.modules.logic_thread.mongo_models import LogicThreadNodeDocument
from api.modules.snap_gap.mongo_models import CoherenceNodeDocument
from api.modules.tap_clues.mongo_models import VocabularyNodeDocument
from api.modules.fact_scanner.mongo_models import ArticleDocument

print("Clearing existing node documents...")
LogicThreadNodeDocument.objects.delete()
CoherenceNodeDocument.objects.delete()
VocabularyNodeDocument.objects.delete()
ArticleDocument.objects.delete()
print("Collections cleared successfully.\n")

# ── LOGIC THREAD NODES ───────────────────────────────────────────────────────
LOGIC_NODES = [
    {
        'node_id': 'log_node_01',
        'title': 'Narration Patterns Basics',
        'focus': 'Mapping basic time-order narrative signals',
        'micro_lesson_text': 'A narration pattern describes events chronologically. Look for first, then, after, and finally.',
        'reading_passage': 'Maria woke up early. First, she reviewed notes. Then she ate breakfast. After arriving at school, she found a seat. Finally, the papers were distributed.',
        'word_count': 26,
        'paragraph_blocks': [
            {'block_id': 'b1', 'text': 'Maria woke up early.', 'order': 1},
            {'block_id': 'b2', 'text': 'First, she reviewed notes.', 'order': 2},
            {'block_id': 'b3', 'text': 'Then she ate breakfast.', 'order': 3},
            {'block_id': 'b4', 'text': 'Finally, she felt ready.', 'order': 4},
        ],
        'correct_sequence': ['b1', 'b2', 'b3', 'b4'],
        'structural_explanations': {
            'b3__b1': 'Block 1 is the opening event and must come first.',
            'b4__b2': 'Finally signals the last step, not the second.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Find the scene setting first.'},
            {'tier': 2, 'hint_text': 'Look for First and Then to order steps.'},
            {'tier': 3, 'hint_text': 'Sequence: opening -> first action -> second -> final.'},
        ]
    },
    {
        'node_id': 'log_node_02',
        'title': 'Narration Patterns Intermediate',
        'focus': 'Sequence events using intermediate markers',
        'micro_lesson_text': 'Intermediate narration uses markers like initially, subsequently, concurrently, and ultimately.',
        'reading_passage': 'Initially, the team gathered requirements. Subsequently, they drafted a blueprint. Concurrently, the developers set up the servers. Ultimately, the product launched.',
        'word_count': 23,
        'paragraph_blocks': [
            {'block_id': 'b1', 'text': 'Initially, the team gathered requirements.', 'order': 1},
            {'block_id': 'b2', 'text': 'Subsequently, they drafted a blueprint.', 'order': 2},
            {'block_id': 'b3', 'text': 'Concurrently, developers set up servers.', 'order': 3},
            {'block_id': 'b4', 'text': 'Ultimately, the product launched.', 'order': 4},
        ],
        'correct_sequence': ['b1', 'b2', 'b3', 'b4'],
        'structural_explanations': {
            'b4__b1': 'Ultimately is a concluding transition and must go last.',
            'b2__b4': 'Subsequently indicates something that follows the opening step.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Initially signals the starting block.'},
            {'tier': 2, 'hint_text': 'Concurrently and subsequently show middle development.'},
            {'tier': 3, 'hint_text': 'Order: Initially -> Subsequently -> Concurrently -> Ultimately.'},
        ]
    },
    {
        'node_id': 'log_node_03',
        'title': 'Narration Patterns Advanced',
        'focus': 'Map complex chronological narrative development',
        'micro_lesson_text': 'Advanced narration weaves prior events, simultaneous actions, and final resolutions smoothly.',
        'reading_passage': 'Long before the launch, research began. Meanwhile, engineers tested the engine. Shortly thereafter, assembly started. In the final analysis, flight succeeded.',
        'word_count': 24,
        'paragraph_blocks': [
            {'block_id': 'b1', 'text': 'Long before the launch, research began.', 'order': 1},
            {'block_id': 'b2', 'text': 'Meanwhile, engineers tested the engine.', 'order': 2},
            {'block_id': 'b3', 'text': 'Shortly thereafter, assembly started.', 'order': 3},
            {'block_id': 'b4', 'text': 'In the final analysis, flight succeeded.', 'order': 4},
        ],
        'correct_sequence': ['b1', 'b2', 'b3', 'b4'],
        'structural_explanations': {
            'b3__b1': 'Research must happen long before assembly.',
            'b4__b2': 'The final flight success must follow testing.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Start with the pre-requisite historical step.'},
            {'tier': 2, 'hint_text': 'Meanwhile connects parallel engineering actions.'},
            {'tier': 3, 'hint_text': 'Sequence: Long before -> Meanwhile -> Shortly thereafter -> Final analysis.'},
        ]
    },
    {
        'node_id': 'log_node_04',
        'title': 'Definition Patterns Basics',
        'focus': 'Identify a simple definition structure',
        'micro_lesson_text': 'A definition introduces a concept and explains what it is. Look for is defined as or refers to.',
        'reading_passage': 'Photosynthesis is defined as the process by which plants use sunlight. Specifically, they convert water and carbon dioxide into oxygen. Thus, it sustains life.',
        'word_count': 26,
        'paragraph_blocks': [
            {'block_id': 'b1', 'text': 'Photosynthesis is defined as a chemical process.', 'order': 1},
            {'block_id': 'b2', 'text': 'Specifically, plants convert sunlight to energy.', 'order': 2},
            {'block_id': 'b3', 'text': 'They release oxygen as a byproduct.', 'order': 3},
            {'block_id': 'b4', 'text': 'Thus, this process sustains global life.', 'order': 4},
        ],
        'correct_sequence': ['b1', 'b2', 'b3', 'b4'],
        'structural_explanations': {
            'b4__b1': 'Thus signals a summary conclusion, not the definition.',
            'b2__b3': 'The converting of sunlight precedes the release of oxygen.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Find the concept definition statement first.'},
            {'tier': 2, 'hint_text': 'Look for details of the chemical conversion.'},
            {'tier': 3, 'hint_text': 'Order: definition -> details -> byproduct -> summary.'},
        ]
    },
    {
        'node_id': 'log_node_05',
        'title': 'Definition Patterns Intermediate',
        'focus': 'Map a multi-part definition with characteristics',
        'micro_lesson_text': 'Intermediate definitions expand concepts through essential traits and illustrative subtypes.',
        'reading_passage': 'Artificial Intelligence refers to machines mimicking human cognition. Its primary traits include learning and reasoning. For instance, expert systems solve problems. Consequently, it remodels industries.',
        'word_count': 27,
        'paragraph_blocks': [
            {'block_id': 'b1', 'text': 'Artificial Intelligence refers to cognitive machines.', 'order': 1},
            {'block_id': 'b2', 'text': 'Its primary traits include learning and reasoning.', 'order': 2},
            {'block_id': 'b3', 'text': 'For instance, expert systems solve problems.', 'order': 3},
            {'block_id': 'b4', 'text': 'Consequently, it remodels modern industries.', 'order': 4},
        ],
        'correct_sequence': ['b1', 'b2', 'b3', 'b4'],
        'structural_explanations': {
            'b3__b1': 'Examples should follow the conceptual definition.',
            'b4__b2': 'The industrial consequence should cap the explanation.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Locate the broad machine cognition definition.'},
            {'tier': 2, 'hint_text': 'Identify the list of cognitive traits next.'},
            {'tier': 3, 'hint_text': 'Order: concept -> traits -> example -> consequence.'},
        ]
    },
    {
        'node_id': 'log_node_06',
        'title': 'Definition Patterns Advanced',
        'focus': 'Map a full academic definition with examples',
        'micro_lesson_text': 'Advanced definitions use technical terminology, distinguish key subfields, and detail utility.',
        'reading_passage': 'Quantum computing is defined by processing via quantum mechanics. Specifically, it employs qubits that represent multiple states simultaneously. This differs from classical binary bits. Therefore, it solves complex cryptography.',
        'word_count': 30,
        'paragraph_blocks': [
            {'block_id': 'b1', 'text': 'Quantum computing utilizes quantum mechanics.', 'order': 1},
            {'block_id': 'b2', 'text': 'Specifically, it employs multi-state qubits.', 'order': 2},
            {'block_id': 'b3', 'text': 'This differs from classical binary bits.', 'order': 3},
            {'block_id': 'b4', 'text': 'Therefore, it solves complex cryptography.', 'order': 4},
        ],
        'correct_sequence': ['b1', 'b2', 'b3', 'b4'],
        'structural_explanations': {
            'b4__b1': 'Cryptography utility is the final conclusion.',
            'b3__b2': 'Contrasting bits must come after introducing qubits.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Start with the fundamental physics definition.'},
            {'tier': 2, 'hint_text': 'Explain qubits before contrasting with binary bits.'},
            {'tier': 3, 'hint_text': 'Order: definition -> mechanism -> contrast -> utility.'},
        ]
    },
    {
        'node_id': 'log_node_07',
        'title': 'Comparison & Contrast Basics',
        'focus': 'Identify simple similarity and difference signals',
        'micro_lesson_text': 'Comparison shows similarity (similarly, likewise). Contrast shows difference (unlike, however).',
        'reading_passage': 'Both cats and dogs make excellent household pets. Similarly, both require regular feeding. Unlike dogs, cats are highly independent. However, both offer great companionship.',
        'word_count': 26,
        'paragraph_blocks': [
            {'block_id': 'b1', 'text': 'Both cats and dogs make excellent pets.', 'order': 1},
            {'block_id': 'b2', 'text': 'Similarly, both require regular feeding.', 'order': 2},
            {'block_id': 'b3', 'text': 'Unlike dogs, cats are highly independent.', 'order': 3},
            {'block_id': 'b4', 'text': 'However, both offer great companionship.', 'order': 4},
        ],
        'correct_sequence': ['b1', 'b2', 'b3', 'b4'],
        'structural_explanations': {
            'b3__b1': 'Establish the joint subject before contrasting them.',
            'b4__b2': 'The final companionship statement rounds out the comparison.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Introduce both subjects first.'},
            {'tier': 2, 'hint_text': 'Follow with similarity, then contrast.'},
            {'tier': 3, 'hint_text': 'Order: introduction -> similarity -> contrast -> resolution.'},
        ]
    },
    {
        'node_id': 'log_node_08',
        'title': 'Comparison & Contrast Intermediate',
        'focus': 'Map a four-part compare and contrast structure',
        'micro_lesson_text': 'Intermediate comparison compares two systems across distinct parameters, highlighting trade-offs.',
        'reading_passage': 'Solar energy and fossil fuels are major power sources. Solar energy is completely renewable. In contrast, fossil fuels are finite and deplete. Nonetheless, fossil fuels provide consistent baseline power.',
        'word_count': 29,
        'paragraph_blocks': [
            {'block_id': 'b1', 'text': 'Solar energy and fossil fuels power society.', 'order': 1},
            {'block_id': 'b2', 'text': 'Solar energy is completely renewable.', 'order': 2},
            {'block_id': 'b3', 'text': 'In contrast, fossil fuels deplete.', 'order': 3},
            {'block_id': 'b4', 'text': 'Nonetheless, fossil fuels provide baseline power.', 'order': 4},
        ],
        'correct_sequence': ['b1', 'b2', 'b3', 'b4'],
        'structural_explanations': {
            'b3__b1': 'Introduce solar/fossil before contrasting depletion.',
            'b4__b2': 'Baseline power trade-off comes after depletion contrast.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Start with the dual energy source introduction.'},
            {'tier': 2, 'hint_text': 'Follow the positive solar trait with negative fossil trait.'},
            {'tier': 3, 'hint_text': 'Order: introduction -> positive trait -> contrast -> trade-off.'},
        ]
    },
    {
        'node_id': 'log_node_09',
        'title': 'Comparison & Contrast Advanced',
        'focus': 'Map a complex multi-criteria comparison text',
        'micro_lesson_text': 'Advanced comparison uses multiple criteria (cost, speed, quality) and evaluates suitability.',
        'reading_passage': 'Traditional and Agile project frameworks organize work. Traditional projects utilize strict sequential planning. Conversely, Agile projects prioritize rapid iterations. While traditional guarantees scope, Agile maximizes market responsiveness.',
        'word_count': 28,
        'paragraph_blocks': [
            {'block_id': 'b1', 'text': 'Traditional and Agile frameworks organize work.', 'order': 1},
            {'block_id': 'b2', 'text': 'Traditional utilize strict sequential planning.', 'order': 2},
            {'block_id': 'b3', 'text': 'Conversely, Agile prioritize rapid iterations.', 'order': 3},
            {'block_id': 'b4', 'text': 'While traditional guarantees scope, Agile responds faster.', 'order': 4},
        ],
        'correct_sequence': ['b1', 'b2', 'b3', 'b4'],
        'structural_explanations': {
            'b3__b1': 'Define Agile iterations after introducing both frameworks.',
            'b4__b2': 'The final summary comparison of scope vs speed comes last.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Introduce frameworks before detailing planning.'},
            {'tier': 2, 'hint_text': 'Use Conversely to contrast sequential with iterative.'},
            {'tier': 3, 'hint_text': 'Order: introduction -> sequential -> iterative -> summary.'},
        ]
    },
    {
        'node_id': 'log_node_10',
        'title': 'Cause & Effect Basics',
        'focus': 'Identify a simple cause and its direct effect',
        'micro_lesson_text': 'A cause-effect pattern explains why things happen. Look for because, therefore, and leads to.',
        'reading_passage': 'Diligent study habits prepare students for exams. Because they review notes, they understand topics. This leads to higher test scores. Therefore, preparation guarantees success.',
        'word_count': 26,
        'paragraph_blocks': [
            {'block_id': 'b1', 'text': 'Diligent study habits prepare students.', 'order': 1},
            {'block_id': 'b2', 'text': 'Because they review, they understand topics.', 'order': 2},
            {'block_id': 'b3', 'text': 'This leads to higher test scores.', 'order': 3},
            {'block_id': 'b4', 'text': 'Therefore, preparation guarantees success.', 'order': 4},
        ],
        'correct_sequence': ['b1', 'b2', 'b3', 'b4'],
        'structural_explanations': {
            'b3__b1': 'Understanding must happen before receiving test scores.',
            'b4__b2': 'The final success claim must be a concluding point.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Introduce study habits first.'},
            {'tier': 2, 'hint_text': 'Link studying to understanding, then scoring.'},
            {'tier': 3, 'hint_text': 'Order: habit -> understanding -> scores -> success.'},
        ]
    },
    {
        'node_id': 'log_node_11',
        'title': 'Cause & Effect Intermediate',
        'focus': 'Map a chained cause-effect academic argument',
        'micro_lesson_text': 'Intermediate cause-effect maps sequential steps where one result becomes the cause of the next.',
        'reading_passage': 'Consistent physical exercise increases cardiovascular efficiency. As a result, muscles receive more oxygenated blood. Consequently, stamina increases during daily activities. Thus, exercise improves vitality.',
        'word_count': 26,
        'paragraph_blocks': [
            {'block_id': 'b1', 'text': 'Consistent physical exercise increases efficiency.', 'order': 1},
            {'block_id': 'b2', 'text': 'As a result, muscles receive oxygen.', 'order': 2},
            {'block_id': 'b3', 'text': 'Consequently, stamina increases.', 'order': 3},
            {'block_id': 'b4', 'text': 'Thus, exercise improves overall vitality.', 'order': 4},
        ],
        'correct_sequence': ['b1', 'b2', 'b3', 'b4'],
        'structural_explanations': {
            'b3__b1': 'Oxygen delivery to muscles must precede stamina increase.',
            'b4__b2': 'Overall vitality is the final outcome of the chain.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Start with the initial exercise cause.'},
            {'tier': 2, 'hint_text': 'Trace blood oxygen -> stamina increase -> vitality.'},
            {'tier': 3, 'hint_text': 'Order: exercise -> oxygen -> stamina -> vitality.'},
        ]
    },
    {
        'node_id': 'log_node_12',
        'title': 'Cause & Effect Advanced',
        'focus': 'Map complex cascading cause-effect relationships',
        'micro_lesson_text': 'Advanced cause-effect details systemic chains where industrial actions trigger global shifts.',
        'reading_passage': 'Industrial factories release high amounts of carbon dioxide. This emission traps solar heat in the atmosphere. Consequently, global ocean temperatures rise steadily. This warming triggers widespread coral bleaching.',
        'word_count': 29,
        'paragraph_blocks': [
            {'block_id': 'b1', 'text': 'Industrial factories release carbon dioxide.', 'order': 1},
            {'block_id': 'b2', 'text': 'This emission traps solar heat.', 'order': 2},
            {'block_id': 'b3', 'text': 'Consequently, ocean temperatures rise.', 'order': 3},
            {'block_id': 'b4', 'text': 'This warming triggers coral bleaching.', 'order': 4},
        ],
        'correct_sequence': ['b1', 'b2', 'b3', 'b4'],
        'structural_explanations': {
            'b4__b1': 'Coral bleaching is the final consequence of ocean warming.',
            'b3__b2': 'Trapping heat must precede ocean temperature rise.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Identify the industrial carbon release first.'},
            {'tier': 2, 'hint_text': 'Connect carbon -> trapped heat -> hot oceans -> bleaching.'},
            {'tier': 3, 'hint_text': 'Order: factories -> heat -> ocean rise -> bleaching.'},
        ]
    },
    {
        'node_id': 'log_node_13',
        'title': 'Narration Patterns Basics 2',
        'focus': 'Identify simple time-order signals in kitchen prep',
        'micro_lesson_text': 'A narration pattern details steps in a recipe. Look for first, next, and finally.',
        'reading_passage': 'Making a sandwich is simple. First, lay out two slices of bread. Next, apply your favorite spread. Finally, press the slices together and enjoy.',
        'word_count': 27,
        'paragraph_blocks': [
            {'block_id': 'b1', 'text': 'Making a sandwich is simple.', 'order': 1},
            {'block_id': 'b2', 'text': 'First, lay out slices of bread.', 'order': 2},
            {'block_id': 'b3', 'text': 'Next, apply your favorite spread.', 'order': 3},
            {'block_id': 'b4', 'text': 'Finally, press slices together.', 'order': 4},
        ],
        'correct_sequence': ['b1', 'b2', 'b3', 'b4'],
        'structural_explanations': {
            'b3__b1': 'Lay bread first before applying spreads.',
            'b4__b2': 'Pressing bread happens after applying spreads.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Find the introductory statement.'},
            {'tier': 2, 'hint_text': 'Use First and Next to arrange prep steps.'},
            {'tier': 3, 'hint_text': 'Order: introduction -> bread -> spread -> press.'},
        ]
    },
]

for node in LOGIC_NODES:
    LogicThreadNodeDocument(**node).save()
    print(f"Seeded: {node['node_id']} — {node['title']}")


# ── SNAP GAP NODES ───────────────────────────────────────────────────────────
SNAP_GAP_NODES = [
    {
        'node_id': 'snp_node_01',
        'title': 'Addition Transitions Basics',
        'focus': 'Identify simple addition transitions',
        'micro_lesson_text': 'Addition transitions add info. Key words: furthermore, additionally, also.',
        'reading_passage': '',
        'word_count': 0,
        'sentence_pairs': [
            {
                'pair_id': 'pair_01',
                'sentence_a': 'Regular exercise improves cardiovascular health.',
                'sentence_b': 'it strengthens muscles and boosts mental well-being.',
            },
            {
                'pair_id': 'pair_02',
                'sentence_a': 'Learning coding develops logical thinking.',
                'sentence_b': 'it opens up diverse career opportunities.',
            }
        ],
        'transition_tile_dock': ['Furthermore', 'However', 'Therefore', 'Additionally', 'Nevertheless', 'Consequentially'],
        'correct_tile_map': {
            'pair_01': 'Furthermore',
            'pair_02': 'Additionally',
        },
        'tile_error_explanations': {
            'pair_01__However': 'However implies contrast, but these ideas agree.',
            'pair_02__Therefore': 'Therefore implies cause-effect, but this is simple addition.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Both sentences add positive points.'},
            {'tier': 2, 'hint_text': 'Use addition tiles like Furthermore and Additionally.'},
            {'tier': 3, 'hint_text': 'Pair 01 gets Furthermore. Pair 02 gets Additionally.'},
        ]
    },
    {
        'node_id': 'snp_node_02',
        'title': 'Addition Transitions Intermediate',
        'focus': 'Use addition and sequence in intermediate contexts',
        'micro_lesson_text': 'Intermediate addition links multiple points with transitions like moreover and in addition.',
        'reading_passage': '',
        'word_count': 0,
        'sentence_pairs': [
            {
                'pair_id': 'pair_01',
                'sentence_a': 'Organic farming avoids chemical pesticides.',
                'sentence_b': 'it promotes biodiversity in soil ecosystems.',
            },
            {
                'pair_id': 'pair_02',
                'sentence_a': 'Solar power plants generate clean electricity.',
                'sentence_b': 'they reduce reliance on local grid systems.',
            }
        ],
        'transition_tile_dock': ['Moreover', 'Conversely', 'Thus', 'In addition', 'Yet', 'Consequently'],
        'correct_tile_map': {
            'pair_01': 'Moreover',
            'pair_02': 'In addition',
        },
        'tile_error_explanations': {
            'pair_01__Conversely': 'Conversely shows contrast, which is inappropriate here.',
            'pair_02__Consequently': 'Consequently implies a direct cause-effect result, but this is an added benefit.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Both sentences list benefits. Look for adding words.'},
            {'tier': 2, 'hint_text': 'Use Moreover for pair 01 and In addition for pair 02.'},
            {'tier': 3, 'hint_text': 'Pair 01: Moreover. Pair 02: In addition.'},
        ]
    },
    {
        'node_id': 'snp_node_03',
        'title': 'Addition Transitions Advanced',
        'focus': 'Apply complex addition transitions academically',
        'micro_lesson_text': 'Advanced addition transitions like besides and likewise weave subtle supporting arguments.',
        'reading_passage': '',
        'word_count': 0,
        'sentence_pairs': [
            {
                'pair_id': 'pair_01',
                'sentence_a': 'The novel critiques industrial modernization.',
                'sentence_b': 'it mirrors the author\'s disillusionment with society.',
            },
            {
                'pair_id': 'pair_02',
                'sentence_a': 'Scientific models simulate climate trajectories.',
                'sentence_b': 'historical records corroborate global temperature increases.',
            }
        ],
        'transition_tile_dock': ['Besides', 'However', 'Therefore', 'Likewise', 'Nonetheless', 'Consequently'],
        'correct_tile_map': {
            'pair_01': 'Besides',
            'pair_02': 'Likewise',
        },
        'tile_error_explanations': {
            'pair_01__However': 'However implies contrast, but these sentences support each other.',
            'pair_02__Therefore': 'Therefore implies direct causation, but this is comparative validation.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look for tiles that expand the literary/scientific focus.'},
            {'tier': 2, 'hint_text': 'Besides adds external author context. Likewise shows parallel validation.'},
            {'tier': 3, 'hint_text': 'Pair 01: Besides. Pair 02: Likewise.'},
        ]
    },
    {
        'node_id': 'snp_node_04',
        'title': 'Contrast Transitions Basics',
        'focus': 'Identify basic contrast transitions',
        'micro_lesson_text': 'Contrast transitions show opposition. Key words: however, on the other hand.',
        'reading_passage': '',
        'word_count': 0,
        'sentence_pairs': [
            {
                'pair_id': 'pair_01',
                'sentence_a': 'Many students believe reading is easy.',
                'sentence_b': 'comprehension tests show significant difficulties.',
            },
            {
                'pair_id': 'pair_02',
                'sentence_a': 'E-books offer immense portability.',
                'sentence_b': 'many readers prefer the feel of paper pages.',
            }
        ],
        'transition_tile_dock': ['However', 'Therefore', 'Furthermore', 'On the other hand', 'Thus', 'Additionally'],
        'correct_tile_map': {
            'pair_01': 'However',
            'pair_02': 'On the other hand',
        },
        'tile_error_explanations': {
            'pair_01__Therefore': 'Therefore shows result, but scores contradict beliefs.',
            'pair_02__Furthermore': 'Furthermore adds info, but these clauses represent contrasting preferences.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Identify the contradiction between belief and reality.'},
            {'tier': 2, 'hint_text': 'Use contrast words: However and On the other hand.'},
            {'tier': 3, 'hint_text': 'Pair 01: However. Pair 02: On the other hand.'},
        ]
    },
    {
        'node_id': 'snp_node_05',
        'title': 'Contrast Transitions Intermediate',
        'focus': 'Use contrast transitions in intermediate contexts',
        'micro_lesson_text': 'Intermediate contrast transitions include conversely and in contrast.',
        'reading_passage': '',
        'word_count': 0,
        'sentence_pairs': [
            {
                'pair_id': 'pair_01',
                'sentence_a': 'Introverted individuals recharge during quiet solitude.',
                'sentence_b': 'extroverts gain energy from social interactions.',
            },
            {
                'pair_id': 'pair_02',
                'sentence_a': 'Inbound marketing pulls interested prospects.',
                'sentence_b': 'outbound marketing pushes messages to cold audiences.',
            }
        ],
        'transition_tile_dock': ['Conversely', 'Moreover', 'Thus', 'In contrast', 'Therefore', 'Besides'],
        'correct_tile_map': {
            'pair_01': 'Conversely',
            'pair_02': 'In contrast',
        },
        'tile_error_explanations': {
            'pair_01__Moreover': 'Moreover adds aligned traits, but introverts and extroverts differ.',
            'pair_02__Thus': 'Thus shows cause-effect, but inbound and outbound are opposing strategies.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look for words comparing opposite personalities or marketing types.'},
            {'tier': 2, 'hint_text': 'Use Conversely for introverts/extroverts and In contrast for marketing.'},
            {'tier': 3, 'hint_text': 'Pair 01: Conversely. Pair 02: In contrast.'},
        ]
    },
    {
        'node_id': 'snp_node_06',
        'title': 'Contrast Transitions Advanced',
        'focus': 'Apply nuanced contrast in academic arguments',
        'micro_lesson_text': 'Advanced contrast transitions like nonetheless and alternatively manage subtle concessions.',
        'reading_passage': '',
        'word_count': 0,
        'sentence_pairs': [
            {
                'pair_id': 'pair_01',
                'sentence_a': 'The experiment failed to yield significant statistics.',
                'sentence_b': 'the collected pilot data indicates promising trends.',
            },
            {
                'pair_id': 'pair_02',
                'sentence_a': 'Governments could implement strict carbon taxation.',
                'sentence_b': 'they could subsidize large-scale clean energy grids.',
            }
        ],
        'transition_tile_dock': ['Nonetheless', 'Therefore', 'Furthermore', 'Alternatively', 'Consequently', 'Likewise'],
        'correct_tile_map': {
            'pair_01': 'Nonetheless',
            'pair_02': 'Alternatively',
        },
        'tile_error_explanations': {
            'pair_01__Consequently': 'Consequently implies a result, but these statements are a concession.',
            'pair_02__Likewise': 'Likewise compares similar items, but these are mutually exclusive options.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Identify options and concessions in the sentence pairs.'},
            {'tier': 2, 'hint_text': 'Nonetheless shows positive concession. Alternatively shows a distinct choice.'},
            {'tier': 3, 'hint_text': 'Pair 01: Nonetheless. Pair 02: Alternatively.'},
        ]
    },
    {
        'node_id': 'snp_node_07',
        'title': 'Cause & Effect Transitions Basics',
        'focus': 'Identify simple cause-effect transitions',
        'micro_lesson_text': 'Cause-effect transitions show consequences. Key words: therefore, consequently.',
        'reading_passage': '',
        'word_count': 0,
        'sentence_pairs': [
            {
                'pair_id': 'pair_01',
                'sentence_a': 'The developer skipped reviewing code updates.',
                'sentence_b': 'she struggled to fix several avoidable bugs.',
            },
            {
                'pair_id': 'pair_02',
                'sentence_a': 'Heavier rain flooded local drainage channels.',
                'sentence_b': 'traffic came to a complete halt.',
            }
        ],
        'transition_tile_dock': ['Therefore', 'However', 'Furthermore', 'Consequently', 'Nevertheless', 'Additionally'],
        'correct_tile_map': {
            'pair_01': 'Therefore',
            'pair_02': 'Consequently',
        },
        'tile_error_explanations': {
            'pair_01__However': 'However shows contrast, but bugs are a direct result of skipping reviews.',
            'pair_02__Furthermore': 'Furthermore adds info, but traffic halts because of floods.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Sentence B happened because of Sentence A.'},
            {'tier': 2, 'hint_text': 'Use Therefore and Consequently to link cause to effect.'},
            {'tier': 3, 'hint_text': 'Pair 01: Therefore. Pair 02: Consequently.'},
        ]
    },
    {
        'node_id': 'snp_node_08',
        'title': 'Cause & Effect Transitions Intermediate',
        'focus': 'Distinguish intermediate cause-effect signals',
        'micro_lesson_text': 'Intermediate cause-effect transitions include as a result and hence.',
        'reading_passage': '',
        'word_count': 0,
        'sentence_pairs': [
            {
                'pair_id': 'pair_01',
                'sentence_a': 'Antibiotics are overprescribed for minor infections.',
                'sentence_b': 'bacteria develop resistance mutations rapidly.',
            },
            {
                'pair_id': 'pair_02',
                'sentence_a': 'The glacier melted at an unprecedented rate.',
                'sentence_b': 'coastal communities experienced heightened sea levels.',
            }
        ],
        'transition_tile_dock': ['As a result', 'Moreover', 'Conversely', 'Hence', 'But', 'Besides'],
        'correct_tile_map': {
            'pair_01': 'As a result',
            'pair_02': 'Hence',
        },
        'tile_error_explanations': {
            'pair_01__Conversely': 'Conversely implies contrast, but mutations result from overprescription.',
            'pair_02__Moreover': 'Moreover adds points, but rising sea level is a consequence.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Link causes (prescription, melting) to consequences.'},
            {'tier': 2, 'hint_text': 'Use As a result for bacterial resistance, Hence for sea level changes.'},
            {'tier': 3, 'hint_text': 'Pair 01: As a result. Pair 02: Hence.'},
        ]
    },
    {
        'node_id': 'snp_node_09',
        'title': 'Cause & Effect Transitions Advanced',
        'focus': 'Apply cause-effect transitions academically',
        'micro_lesson_text': 'Advanced cause-effect transitions like thus and accordingly demonstrate analytical proof.',
        'reading_passage': '',
        'word_count': 0,
        'sentence_pairs': [
            {
                'pair_id': 'pair_01',
                'sentence_a': 'The mathematical proof resolved the foundational paradox.',
                'sentence_b': 'it paved the way for modern computing logic.',
            },
            {
                'pair_id': 'pair_02',
                'sentence_a': 'Participants reported severe allergic reactions.',
                'sentence_b': 'the research team suspended clinical evaluations.',
            }
        ],
        'transition_tile_dock': ['Thus', 'Conversely', 'Furthermore', 'Accordingly', 'Nonetheless', 'Besides'],
        'correct_tile_map': {
            'pair_01': 'Thus',
            'pair_02': 'Accordingly',
        },
        'tile_error_explanations': {
            'pair_01__Conversely': 'Conversely implies contrast, but computing logic is a result.',
            'pair_02__Furthermore': 'Furthermore adds info, but team response is a consequence.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look for logical deductions and administrative consequences.'},
            {'tier': 2, 'hint_text': 'Thus shows logical consequence. Accordingly shows appropriate action taken.'},
            {'tier': 3, 'hint_text': 'Pair 01: Thus. Pair 02: Accordingly.'},
        ]
    },
    {
        'node_id': 'snp_node_10',
        'title': 'Conclusion Transitions Basics',
        'focus': 'Identify basic conclusion transitions',
        'micro_lesson_text': 'Conclusion transitions signal summaries. Key words: ultimately, in conclusion.',
        'reading_passage': '',
        'word_count': 0,
        'sentence_pairs': [
            {
                'pair_id': 'pair_01',
                'sentence_a': 'The team revised designs and optimized code.',
                'sentence_b': 'the system launched with zero errors.',
            },
            {
                'pair_id': 'pair_02',
                'sentence_a': 'Data proves that interactive study boosts marks.',
                'sentence_b': 'schools should integrate digital learning tools.',
            }
        ],
        'transition_tile_dock': ['Ultimately', 'However', 'Additionally', 'In conclusion', 'Yet', 'Furthermore'],
        'correct_tile_map': {
            'pair_01': 'Ultimately',
            'pair_02': 'In conclusion',
        },
        'tile_error_explanations': {
            'pair_01__However': 'However implies contrast, which opposes the successful launch.',
            'pair_02__Furthermore': 'Furthermore adds points, but this is a final recommendation.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Identify final outcomes and summaries.'},
            {'tier': 2, 'hint_text': 'Use Ultimately for outcomes, In conclusion for summaries.'},
            {'tier': 3, 'hint_text': 'Pair 01: Ultimately. Pair 02: In conclusion.'},
        ]
    },
    {
        'node_id': 'snp_node_11',
        'title': 'Conclusion Transitions Intermediate',
        'focus': 'Apply intermediate conclusion transitions',
        'micro_lesson_text': 'Intermediate conclusion transitions include to summarize and in summary.',
        'reading_passage': '',
        'word_count': 0,
        'sentence_pairs': [
            {
                'pair_id': 'pair_01',
                'sentence_a': 'Trees provide shade, produce oxygen, and anchor soil.',
                'sentence_b': 'forest preservation protects critical natural infrastructure.',
            },
            {
                'pair_id': 'pair_02',
                'sentence_a': 'Reading daily enhances focus and expands vocabulary.',
                'sentence_b': 'it remains a foundational academic habit.',
            }
        ],
        'transition_tile_dock': ['To summarize', 'Moreover', 'Conversely', 'In summary', 'Therefore', 'Yet'],
        'correct_tile_map': {
            'pair_01': 'To summarize',
            'pair_02': 'In summary',
        },
        'tile_error_explanations': {
            'pair_01__Conversely': 'Conversely implies opposition, which fails to wrap up benefits.',
            'pair_02__Moreover': 'Moreover adds more details, but this wraps up the habit description.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Find phrases that wrap up lists of benefits.'},
            {'tier': 2, 'hint_text': 'Use To summarize for forest structures, In summary for reading habits.'},
            {'tier': 3, 'hint_text': 'Pair 01: To summarize. Pair 02: In summary.'},
        ]
    },
    {
        'node_id': 'snp_node_12',
        'title': 'Conclusion Transitions Advanced',
        'focus': 'Apply advanced conclusion signals academically',
        'micro_lesson_text': 'Advanced conclusion transitions include overall and in final analysis.',
        'reading_passage': '',
        'word_count': 0,
        'sentence_pairs': [
            {
                'pair_id': 'pair_01',
                'sentence_a': 'Test results show high engagement and low churn.',
                'sentence_b': 'the gamified platform is highly successful.',
            },
            {
                'pair_id': 'pair_02',
                'sentence_a': 'The economic index factors in debt, inflation, and growth.',
                'sentence_b': 'reforms are necessary to stabilize national finance.',
            }
        ],
        'transition_tile_dock': ['Overall', 'However', 'Furthermore', 'In final analysis', 'Nonetheless', 'Consequently'],
        'correct_tile_map': {
            'pair_01': 'Overall',
            'pair_02': 'In final analysis',
        },
        'tile_error_explanations': {
            'pair_01__However': 'However implies contrast, but successful metrics align.',
            'pair_02__Furthermore': 'Furthermore adds info, but this is a final reform directive.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Identify sweeping final assessments and structural reform suggestions.'},
            {'tier': 2, 'hint_text': 'Use Overall for system metrics, In final analysis for national reforms.'},
            {'tier': 3, 'hint_text': 'Pair 01: Overall. Pair 02: In final analysis.'},
        ]
    },
    {
        'node_id': 'snp_node_13',
        'title': 'Addition Transitions Basics 2',
        'focus': 'Identify basic addition transitions in a sequence',
        'micro_lesson_text': 'Addition transitions add extra items to a list. Key words: furthermore, also.',
        'reading_passage': '',
        'word_count': 0,
        'sentence_pairs': [
            {
                'pair_id': 'pair_01',
                'sentence_a': 'Cooking at home is generally more cost-efficient.',
                'sentence_b': 'it allows complete control over dietary ingredients.',
            },
            {
                'pair_id': 'pair_02',
                'sentence_a': 'Hiking strengthens leg muscles and burns calories.',
                'sentence_b': 'it provides refreshing exposure to outdoor scenery.',
            }
        ],
        'transition_tile_dock': ['Furthermore', 'However', 'Therefore', 'Also', 'Nevertheless', 'Consequently'],
        'correct_tile_map': {
            'pair_01': 'Furthermore',
            'pair_02': 'Also',
        },
        'tile_error_explanations': {
            'pair_01__However': 'However implies contrast, but these are both benefits of cooking.',
            'pair_02__Therefore': 'Therefore implies causation, but scenic exposure is an added plus.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look for positive additions to home cooking and hiking.'},
            {'tier': 2, 'hint_text': 'Use Furthermore for cooking, Also for hiking.'},
            {'tier': 3, 'hint_text': 'Pair 01: Furthermore. Pair 02: Also.'},
        ]
    },
]

for node in SNAP_GAP_NODES:
    CoherenceNodeDocument(**node).save()
    print(f"Seeded: {node['node_id']} — {node['title']}")


# ── TAP THE CLUES NODES ───────────────────────────────────────────────────────
TAP_CLUES_NODES = [
    {
        'node_id': 'tap_node_01',
        'title': 'Synonym Clues Basics',
        'focus': 'Find synonym clues right beside the word',
        'micro_lesson_text': 'Synonym clues give nearby words with identical meanings. Look for commas, dashes, or "or".',
        'reading_passage': 'The scientist\'s findings were met with skepticism — doubt and disbelief — by her peers, who demanded more rigorous evidence before accepting her conclusions.',
        'word_count': 23,
        'locked_words': [
            {
                'word_id': 'w1',
                'word': 'skepticism',
                'position_index': 5,
                'correct_clue_ids': ['doubt', 'disbelief'],
                'definition': 'Doubt or disbelief about the truth of something.',
                'contextual_usage': 'The proposal was received with skepticism.',
                'translation': 'pag-aalinlangan'
            }
        ],
        'clue_error_explanations': {
            'w1__scientist': 'Scientist is the subject and doesn\'t define skepticism.',
            'w1__evidence': 'Evidence is what was requested, not a synonym of skepticism.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look inside the dashes right after skepticism.'},
            {'tier': 2, 'hint_text': 'Synonyms are doubt and disbelief.'},
            {'tier': 3, 'hint_text': 'Tap doubt and disbelief.'},
        ]
    },
    {
        'node_id': 'tap_node_02',
        'title': 'Synonym Clues Intermediate',
        'focus': 'Find synonym clues in intermediate passages',
        'micro_lesson_text': 'Intermediate synonym clues use phrases like also known as or in other words.',
        'reading_passage': 'The team performed a close scrutiny, in other words, an inspection and examination of the damaged wing, discovering structural failure.',
        'word_count': 20,
        'locked_words': [
            {
                'word_id': 'w1',
                'word': 'scrutiny',
                'position_index': 5,
                'correct_clue_ids': ['inspection', 'examination'],
                'definition': 'Critical and detailed observation or examination.',
                'contextual_usage': 'The documents underwent close scrutiny.',
                'translation': 'pagsusuri'
            }
        ],
        'clue_error_explanations': {
            'w1__team': 'Team is the actor, not a synonym.',
            'w1__damaged': 'Damaged describes the wing, not the act of inspection.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look after the phrase "in other words".'},
            {'tier': 2, 'hint_text': 'Find two words meaning detailed checking.'},
            {'tier': 3, 'hint_text': 'Tap inspection and examination.'},
        ]
    },
    {
        'node_id': 'tap_node_03',
        'title': 'Synonym Clues Advanced',
        'focus': 'Unlock words using advanced synonym context',
        'micro_lesson_text': 'Advanced synonym clues are woven into parallel clauses or sentence pairings.',
        'reading_passage': 'She took a pragmatic approach. Her practical and realistic decisions resolved the crisis, earning praise from the executive board.',
        'word_count': 18,
        'locked_words': [
            {
                'word_id': 'w1',
                'word': 'pragmatic',
                'position_index': 3,
                'correct_clue_ids': ['practical', 'realistic'],
                'definition': 'Dealing with things sensibly and realistically.',
                'contextual_usage': 'We need a pragmatic solution to this problem.',
                'translation': 'praktikal'
            }
        ],
        'clue_error_explanations': {
            'w1__approach': 'Approach is the noun modified, not the definition synonym.',
            'w1__crisis': 'Crisis is the issue solved, not a synonym of pragmatic.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look at the description in the second sentence.'},
            {'tier': 2, 'hint_text': 'Find adjectives meaning sensible or real.'},
            {'tier': 3, 'hint_text': 'Tap practical and realistic.'},
        ]
    },
    {
        'node_id': 'tap_node_04',
        'title': 'Definition Clues Basics',
        'focus': 'Spot a single embedded definition clue',
        'micro_lesson_text': 'Definition clues directly state meanings. Look for defined as or refers to.',
        'reading_passage': 'Bias, which is defined as a tendency to favor one side unfairly, continues to distort media coverage of the election.',
        'word_count': 19,
        'locked_words': [
            {
                'word_id': 'w1',
                'word': 'bias',
                'position_index': 0,
                'correct_clue_ids': ['tendency', 'favor'],
                'definition': 'An inclination to favor one side or perspective unfairly.',
                'contextual_usage': 'The article showed a clear bias.',
                'translation': 'pagkiling'
            }
        ],
        'clue_error_explanations': {
            'w1__coverage': 'Coverage describes the media report, not bias.',
            'w1__election': 'Election is the event, not the definition.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look for clauses starting with defined as.'},
            {'tier': 2, 'hint_text': 'Find words describing an unfair preference.'},
            {'tier': 3, 'hint_text': 'Tap tendency and favor.'},
        ]
    },
    {
        'node_id': 'tap_node_05',
        'title': 'Definition Clues Intermediate',
        'focus': 'Find definition clues in intermediate contexts',
        'micro_lesson_text': 'Intermediate definition clues embed definitions in parenthetical or descriptive structures.',
        'reading_passage': 'They practiced altruism (meaning selflessness and generosity) daily, donating foods and blankets to families displaced by the fire.',
        'word_count': 18,
        'locked_words': [
            {
                'word_id': 'w1',
                'word': 'altruism',
                'position_index': 2,
                'correct_clue_ids': ['selflessness', 'generosity'],
                'definition': 'Disinterested and selfless concern for the well-being of others.',
                'contextual_usage': 'Her altruism inspired many people.',
                'translation': 'pagkabukas-palad'
            }
        ],
        'clue_error_explanations': {
            'w1__donating': 'Donating is the action, not the exact definition.',
            'w1__families': 'Families are the recipients, not the definition of altruism.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look inside the parentheses right after altruism.'},
            {'tier': 2, 'hint_text': 'The definition words describe giving and selflessness.'},
            {'tier': 3, 'hint_text': 'Tap selflessness and generosity.'},
        ]
    },
    {
        'node_id': 'tap_node_06',
        'title': 'Definition Clues Advanced',
        'focus': 'Unlock words using advanced definition clues',
        'micro_lesson_text': 'Advanced definition clues integrate defining characteristics smoothly within complex sentences.',
        'reading_passage': 'The classroom was filled with a cacophony, characterized by loud noise and discordance, making it impossible for students to study.',
        'word_count': 19,
        'locked_words': [
            {
                'word_id': 'w1',
                'word': 'cacophony',
                'position_index': 6,
                'correct_clue_ids': ['noise', 'discordance'],
                'definition': 'A harsh, discordant mixture of sounds.',
                'contextual_usage': 'A cacophony of car horns woke us.',
                'translation': 'ingay'
            }
        ],
        'clue_error_explanations': {
            'w1__classroom': 'Classroom is the setting, not the noise description.',
            'w1__impossible': 'Impossible describes the state of study, not cacophony.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look after the word "characterized by".'},
            {'tier': 2, 'hint_text': 'Select words describing harsh sound or chaos.'},
            {'tier': 3, 'hint_text': 'Tap noise and discordance.'},
        ]
    },
    {
        'node_id': 'tap_node_07',
        'title': 'Antonym Clues Basics',
        'focus': 'Find antonym clues near the word',
        'micro_lesson_text': 'Antonym clues give opposite meanings. Look for but, however, or unlike.',
        'reading_passage': 'Unlike her verbose classmates, Ana\'s presentation was concise and had great brevity, wasting not a single word.',
        'word_count': 17,
        'locked_words': [
            {
                'word_id': 'w1',
                'word': 'verbose',
                'position_index': 2,
                'correct_clue_ids': ['concise', 'brevity'],
                'definition': 'Using more words than needed; wordy.',
                'contextual_usage': 'His verbose explanation was confusing.',
                'translation': 'madaldal'
            }
        ],
        'clue_error_explanations': {
            'w1__presentation': 'Presentation is the activity, not the opposite trait.',
            'w1__classmates': 'Classmates are the speakers compared, not an antonym.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look for descriptors of Ana\'s presentation compared to classmates.'},
            {'tier': 2, 'hint_text': 'Opposite of verbose means short and concise.'},
            {'tier': 3, 'hint_text': 'Tap concise and brevity.'},
        ]
    },
    {
        'node_id': 'tap_node_08',
        'title': 'Antonym Clues Intermediate',
        'focus': 'Find antonym clues in intermediate contexts',
        'micro_lesson_text': 'Intermediate antonym clues use phrases like in contrast or rather than.',
        'reading_passage': 'Rather than being indolent, the puppy was highly active and industrious, running around the yard for hours.',
        'word_count': 18,
        'locked_words': [
            {
                'word_id': 'w1',
                'word': 'indolent',
                'position_index': 3,
                'correct_clue_ids': ['active', 'industrious'],
                'definition': 'Wanting to avoid exertion; lazy.',
                'contextual_usage': 'They lost their jobs because they were indolent.',
                'translation': 'tamad'
            }
        ],
        'clue_error_explanations': {
            'w1__puppy': 'Puppy is the subject, not the trait.',
            'w1__hours': 'Hours is the duration, not the opposite trait.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Find opposite traits that contrast with indolent.'},
            {'tier': 2, 'hint_text': 'Look for words describing high energy.'},
            {'tier': 3, 'hint_text': 'Tap active and industrious.'},
        ]
    },
    {
        'node_id': 'tap_node_09',
        'title': 'Antonym Clues Advanced',
        'focus': 'Unlock words using advanced antonym context',
        'micro_lesson_text': 'Advanced antonyms are structured in comparative clauses with nuanced grammar.',
        'reading_passage': 'The beauty was not ephemeral; instead, it proved permanent and eternal, remaining unchanged over many decades.',
        'word_count': 16,
        'locked_words': [
            {
                'word_id': 'w1',
                'word': 'ephemeral',
                'position_index': 4,
                'correct_clue_ids': ['permanent', 'eternal'],
                'definition': 'Lasting for a very short time.',
                'contextual_usage': 'Fashions are ephemeral, but style lasts.',
                'translation': 'panandalian'
            }
        ],
        'clue_error_explanations': {
            'w1__beauty': 'Beauty is the subject described, not the antonym.',
            'w1__decades': 'Decades is the timeframe, not the antonym word.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Find words in the second clause that contrast with "not ephemeral".'},
            {'tier': 2, 'hint_text': 'Look for adjectives meaning everlasting.'},
            {'tier': 3, 'hint_text': 'Tap permanent and eternal.'},
        ]
    },
    {
        'node_id': 'tap_node_10',
        'title': 'Inference Clues Basics',
        'focus': 'Infer word meaning from one nearby example',
        'micro_lesson_text': 'Inference clues describe a scenario that lets you guess the meaning of a word.',
        'reading_passage': 'The students paced the hallways nervously and whispered anxiously, showing clear consternation after the grades were published.',
        'word_count': 18,
        'locked_words': [
            {
                'word_id': 'w1',
                'word': 'consternation',
                'position_index': 9,
                'correct_clue_ids': ['nervously', 'anxiously'],
                'definition': 'Feelings of anxiety or dismay, typically at something unexpected.',
                'contextual_usage': 'The announcement caused great consternation.',
                'translation': 'pagkabagabag'
            }
        ],
        'clue_error_explanations': {
            'w1__students': 'Students are the actors, not the emotion descriptors.',
            'w1__grades': 'Grades caused the reaction, they are not clues.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Find words describing how the students paced or whispered.'},
            {'tier': 2, 'hint_text': 'Look for adverbs showing worry.'},
            {'tier': 3, 'hint_text': 'Tap nervously and anxiously.'},
        ]
    },
    {
        'node_id': 'tap_node_11',
        'title': 'Inference Clues Intermediate',
        'focus': 'Infer meaning from intermediate example clues',
        'micro_lesson_text': 'Intermediate inference uses descriptive actions in preceding sentences to suggest traits.',
        'reading_passage': 'She fought courageously and stood resolutely in the battle. Everyone praised her fortitude during the difficult struggle.',
        'word_count': 18,
        'locked_words': [
            {
                'word_id': 'w1',
                'word': 'fortitude',
                'position_index': 11,
                'correct_clue_ids': ['courageously', 'resolutely'],
                'definition': 'Courage in pain or adversity.',
                'contextual_usage': 'She showed mental fortitude during the test.',
                'translation': 'katatagan'
            }
        ],
        'clue_error_explanations': {
            'w1__fought': 'Fought is the action, not the manner describing fortitude.',
            'w1__struggle': 'Struggle is the event, not the inner trait.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look at the adverbs in the first sentence.'},
            {'tier': 2, 'hint_text': 'Find adverbs indicating brave behavior.'},
            {'tier': 3, 'hint_text': 'Tap courageously and resolutely.'},
        ]
    },
    {
        'node_id': 'tap_node_12',
        'title': 'Inference Clues Advanced',
        'focus': 'Unlock words using advanced inference clues',
        'micro_lesson_text': 'Advanced inference relies on analyzing complex cause-effect narratives to extract state values.',
        'reading_passage': 'Hanging unsafely on the rope and climbing dangerously on cliffs, the climber realized his precarious position was untenable.',
        'word_count': 18,
        'locked_words': [
            {
                'word_id': 'w1',
                'word': 'precarious',
                'position_index': 13,
                'correct_clue_ids': ['unsafely', 'dangerously'],
                'definition': 'Not securely held or in position; dangerously likely to fall.',
                'contextual_usage': 'The ladder was in a precarious angle.',
                'translation': 'peligroso'
            }
        ],
        'clue_error_explanations': {
            'w1__rope': 'Rope is the object held, not the manner descriptor.',
            'w1__untenable': 'Untenable is a synonym of precarious in logic but not the direct inference clue.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look at how the climber hung on the rope or climbed cliffs.'},
            {'tier': 2, 'hint_text': 'Find adverbs suggesting risk.'},
            {'tier': 3, 'hint_text': 'Tap unsafely and dangerously.'},
        ]
    },
    {
        'node_id': 'tap_node_13',
        'title': 'Synonym Clues Basics 2',
        'focus': 'Identify basic synonym clues in simple descriptions',
        'micro_lesson_text': 'Synonym clues restate meaning using close adjectives. Look for or or dashes.',
        'reading_passage': 'The new student was amiable — friendly and affable — making friends quickly on his very first day.',
        'word_count': 17,
        'locked_words': [
            {
                'word_id': 'w1',
                'word': 'amiable',
                'position_index': 4,
                'correct_clue_ids': ['friendly', 'affable'],
                'definition': 'Having or displaying a friendly and pleasant manner.',
                'contextual_usage': 'An amiable host makes everyone comfortable.',
                'translation': 'mesiyal'
            }
        ],
        'clue_error_explanations': {
            'w1__student': 'Student is the noun modified, not the synonym.',
            'w1__friends': 'Friends is the result of being amiable.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look inside the dashes right after amiable.'},
            {'tier': 2, 'hint_text': 'Amiable synonyms are friendly and affable.'},
            {'tier': 3, 'hint_text': 'Tap friendly and affable.'},
        ]
    },
]

for node in TAP_CLUES_NODES:
    VocabularyNodeDocument(**node).save()
    print(f"Seeded: {node['node_id']} — {node['title']}")


# ── FACT SCANNER NODES ────────────────────────────────────────────────────────
FACT_SCANNER_NODES = [
    {
        'node_id': 'fac_node_01',
        'title': 'Currency Basics',
        'focus': 'Spot a very obviously outdated source',
        'craap_criterion': 'CURRENCY',
        'micro_lesson_text': 'Currency checks if info is recent. Beware predictions using extremely old sources.',
        'reading_passage': 'Climate change requires immediate action. According to a 1975 study, the Earth will experience minimal warming. Renewable energy has accelerated.',
        'word_count': 22,
        'article_sentences': [
            {'sentence_id': 's1', 'text': 'Climate change requires immediate action.', 'is_flawed': False, 'flaw_reason': ''},
            {'sentence_id': 's2', 'text': 'According to a 1975 study, the Earth will experience minimal warming.', 'is_flawed': True, 'flaw_reason': 'Uses a 1975 study for current climate science, violating Currency.'},
            {'sentence_id': 's3', 'text': 'Renewable energy adoption has accelerated.', 'is_flawed': False, 'flaw_reason': ''},
        ],
        'sentence_explanations': {
            's1': 'This is a standard current statement.',
            's3': 'This aligns with recent global trends.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'One sentence relies on a study from the 1970s.'},
            {'tier': 2, 'hint_text': 'Climate predictions from 50 years ago fail Currency.'},
            {'tier': 3, 'hint_text': 'Sentence s2 is the flawed one.'},
        ]
    },
    {
        'node_id': 'fac_node_02',
        'title': 'Currency Intermediate',
        'focus': 'Identify a moderately outdated source',
        'craap_criterion': 'CURRENCY',
        'micro_lesson_text': 'Intermediate currency inspects references for rapidly changing fields like technology.',
        'reading_passage': 'Web design relies on user-centered principles. Developers must consult a 2005 software guide to optimize layouts. Modern sites prioritize mobile responsive designs.',
        'word_count': 24,
        'article_sentences': [
            {'sentence_id': 's1', 'text': 'Web design relies on user-centered principles.', 'is_flawed': False, 'flaw_reason': ''},
            {'sentence_id': 's2', 'text': 'Developers must consult a 2005 software guide to optimize layouts.', 'is_flawed': True, 'flaw_reason': 'Consulting a 2005 software guide for web design violates Currency.'},
            {'sentence_id': 's3', 'text': 'Modern sites prioritize mobile responsive designs.', 'is_flawed': False, 'flaw_reason': ''},
        ],
        'sentence_explanations': {
            's1': 'This remains true in contemporary UI design.',
            's3': 'Mobile responsive design is a standard practice now.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look for technology guidance from 20 years ago.'},
            {'tier': 2, 'hint_text': 'A 2005 guide for modern layout optimization is obsolete.'},
            {'tier': 3, 'hint_text': 'Sentence s2 is outdated. Quarantine it.'},
        ]
    },
    {
        'node_id': 'fac_node_03',
        'title': 'Currency Advanced',
        'focus': 'Detect a subtly outdated claim',
        'craap_criterion': 'CURRENCY',
        'micro_lesson_text': 'Advanced currency detects subtle claims that ignore recent major legislative or market changes.',
        'reading_passage': 'International trade agreements shape global markets. Analysts predict tax exemptions based on a 2018 policy report. Recent tariffs have shifted trading hubs.',
        'word_count': 23,
        'article_sentences': [
            {'sentence_id': 's1', 'text': 'International trade agreements shape global markets.', 'is_flawed': False, 'flaw_reason': ''},
            {'sentence_id': 's2', 'text': 'Analysts predict tax exemptions based on a 2018 policy report.', 'is_flawed': True, 'flaw_reason': 'Predicting taxes in 2026 based on a 2018 report ignores massive recent changes, violating Currency.'},
            {'sentence_id': 's3', 'text': 'Recent tariffs have shifted trading hubs.', 'is_flawed': False, 'flaw_reason': ''},
        ],
        'sentence_explanations': {
            's1': 'This is a general economic truth.',
            's3': 'This is accurate regarding recent geopolitical developments.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'One sentence makes a prediction using a policy report from several years ago.'},
            {'tier': 2, 'hint_text': 'Using 2018 tax policies to predict current exemptions is outdated.'},
            {'tier': 3, 'hint_text': 'Sentence s2 fails Currency. Quarantine it.'},
        ]
    },
    {
        'node_id': 'fac_node_04',
        'title': 'Relevance Basics',
        'focus': 'Spot a completely off-topic sentence',
        'craap_criterion': 'RELEVANCE',
        'micro_lesson_text': 'Relevance checks topic alignment. Off-topic sentences fail this test.',
        'reading_passage': 'Critical reading is essential for academic success. The history of football in the Philippines dates to colonial times. Active readers evaluate sources.',
        'word_count': 23,
        'article_sentences': [
            {'sentence_id': 's1', 'text': 'Critical reading is essential for academic success.', 'is_flawed': False, 'flaw_reason': ''},
            {'sentence_id': 's2', 'text': 'The history of football in the Philippines dates to colonial times.', 'is_flawed': True, 'flaw_reason': 'Football history has no relevance to academic critical reading.'},
            {'sentence_id': 's3', 'text': 'Active readers evaluate sources.', 'is_flawed': False, 'flaw_reason': ''},
        ],
        'sentence_explanations': {
            's1': 'This introduces the central topic.',
            's3': 'This supports the central topic.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'One sentence is about a sport instead of reading.'},
            {'tier': 2, 'hint_text': 'Football history is completely off-topic.'},
            {'tier': 3, 'hint_text': 'Sentence s2 is irrelevant.'},
        ]
    },
    {
        'node_id': 'fac_node_05',
        'title': 'Relevance Intermediate',
        'focus': 'Identify a moderately off-topic sentence',
        'craap_criterion': 'RELEVANCE',
        'micro_lesson_text': 'Intermediate relevance detects descriptions of related activities that deviate from the specific thesis.',
        'reading_passage': 'Solar panels convert solar energy to electricity. Preparing dinner in a solar oven requires slow cooking. This technology reduces carbon emissions.',
        'word_count': 22,
        'article_sentences': [
            {'sentence_id': 's1', 'text': 'Solar panels convert solar energy to electricity.', 'is_flawed': False, 'flaw_reason': ''},
            {'sentence_id': 's2', 'text': 'Preparing dinner in a solar oven requires slow cooking.', 'is_flawed': True, 'flaw_reason': 'Cooking details are irrelevant to solar electricity panels.'},
            {'sentence_id': 's3', 'text': 'This technology reduces carbon emissions.', 'is_flawed': False, 'flaw_reason': ''},
        ],
        'sentence_explanations': {
            's1': 'This is the main topic of solar panels.',
            's3': 'This evaluates the environmental impact of solar panels.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look for cooking details in a solar grid passage.'},
            {'tier': 2, 'hint_text': 'Solar oven dinner recipes are irrelevant to solar panels.'},
            {'tier': 3, 'hint_text': 'Sentence s2 is irrelevant.'},
        ]
    },
    {
        'node_id': 'fac_node_06',
        'title': 'Relevance Advanced',
        'focus': 'Detect a subtly irrelevant sentence',
        'craap_criterion': 'RELEVANCE',
        'micro_lesson_text': 'Advanced relevance isolates corporate or personal details that distract from institutional goals.',
        'reading_passage': 'Our company aims to engineer affordable electric cars. The CEO\'s salary rose by fifteen percent last quarter. Developing battery capacity remains our priority.',
        'word_count': 23,
        'article_sentences': [
            {'sentence_id': 's1', 'text': 'Our company aims to engineer affordable electric cars.', 'is_flawed': False, 'flaw_reason': ''},
            {'sentence_id': 's2', 'text': 'The CEO\'s salary rose by fifteen percent last quarter.', 'is_flawed': True, 'flaw_reason': 'CEO salary changes are irrelevant to corporate engineering goals.'},
            {'sentence_id': 's3', 'text': 'Developing battery capacity remains our priority.', 'is_flawed': False, 'flaw_reason': ''},
        ],
        'sentence_explanations': {
            's1': 'This states the company mission.',
            's3': 'This details specific technical priorities.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look for private compensation details in a car mission text.'},
            {'tier': 2, 'hint_text': 'CEO salary increases are irrelevant to engineering priorities.'},
            {'tier': 3, 'hint_text': 'Sentence s2 is irrelevant.'},
        ]
    },
    {
        'node_id': 'fac_node_07',
        'title': 'Authority Basics',
        'focus': 'Spot an obviously unverified claim',
        'craap_criterion': 'AUTHORITY',
        'micro_lesson_text': 'Authority checks credentials. Avoid anonymous assertions like "experts say".',
        'reading_passage': 'Immunization prevents diseases globally. Experts say that vaccines cause more harm than good and should be avoided. The WHO recommends child vaccinations.',
        'word_count': 23,
        'article_sentences': [
            {'sentence_id': 's1', 'text': 'Immunization prevents diseases globally.', 'is_flawed': False, 'flaw_reason': ''},
            {'sentence_id': 's2', 'text': 'Experts say that vaccines cause more harm than good and should be avoided.', 'is_flawed': True, 'flaw_reason': 'Cites vague "experts say" without credentials, violating Authority.'},
            {'sentence_id': 's3', 'text': 'The WHO recommends child vaccinations.', 'is_flawed': False, 'flaw_reason': ''},
        ],
        'sentence_explanations': {
            's1': 'This is a historically verified fact.',
            's3': 'The WHO is a named, credible global authority.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look for statements starting with "Experts say" without naming anyone.'},
            {'tier': 2, 'hint_text': 'Vague experts making vaccine claims fails Authority.'},
            {'tier': 3, 'hint_text': 'Sentence s2 is flawed.'},
        ]
    },
    {
        'node_id': 'fac_node_08',
        'title': 'Authority Intermediate',
        'focus': 'Identify a moderately unverified source',
        'craap_criterion': 'AUTHORITY',
        'micro_lesson_text': 'Intermediate authority detects citations from random blogs rather than peer-reviewed consensus.',
        'reading_passage': 'Astrophysicists study cosmic microwave background radiation. According to a comment on a popular forum, black holes contain portals to other dimensions. Peer-reviewed studies support gravitational theories.',
        'word_count': 26,
        'article_sentences': [
            {'sentence_id': 's1', 'text': 'Astrophysicists study cosmic microwave background radiation.', 'is_flawed': False, 'flaw_reason': ''},
            {'sentence_id': 's2', 'text': 'According to a comment on a popular forum, black holes contain portals.', 'is_flawed': True, 'flaw_reason': 'Citing a random forum comment for astrophysics violates Authority.'},
            {'sentence_id': 's3', 'text': 'Peer-reviewed studies support gravitational theories.', 'is_flawed': False, 'flaw_reason': ''},
        ],
        'sentence_explanations': {
            's1': 'This is a standard description of astrophysics.',
            's3': 'Peer-reviewed research represents valid authority.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look for a scientific claim citing a forum comment.'},
            {'tier': 2, 'hint_text': 'A forum post lacks academic credentials for black hole theory.'},
            {'tier': 3, 'hint_text': 'Sentence s2 is flawed.'},
        ]
    },
    {
        'node_id': 'fac_node_09',
        'title': 'Authority Advanced',
        'focus': 'Detect a subtly unqualified claim',
        'craap_criterion': 'AUTHORITY',
        'micro_lesson_text': 'Advanced authority exposes celebrity opinions used to validate technical or economic policies.',
        'reading_passage': 'Macroeconomic policy helps regulate national interest rates. A famous movie actor warns that central banking models lead to instant hyperinflation. Academic economists debate quantitative easing.',
        'word_count': 26,
        'article_sentences': [
            {'sentence_id': 's1', 'text': 'Macroeconomic policy helps regulate national interest rates.', 'is_flawed': False, 'flaw_reason': ''},
            {'sentence_id': 's2', 'text': 'A famous movie actor warns that central banking models lead to instant hyperinflation.', 'is_flawed': True, 'flaw_reason': 'Actors lack economics credentials, violating Authority.'},
            {'sentence_id': 's3', 'text': 'Academic economists debate quantitative easing.', 'is_flawed': False, 'flaw_reason': ''},
        ],
        'sentence_explanations': {
            's1': 'This describes standard economic management.',
            's3': 'Academic economists are valid authorities on banking.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look for a movie actor advising on banking models.'},
            {'tier': 2, 'hint_text': 'An actor has no professional authority in macroeconomics.'},
            {'tier': 3, 'hint_text': 'Sentence s2 fails Authority.'},
        ]
    },
    {
        'node_id': 'fac_node_10',
        'title': 'Accuracy Basics',
        'focus': 'Spot a wildly inaccurate claim',
        'craap_criterion': 'ACCURACY',
        'micro_lesson_text': 'Accuracy verifies factuality. Expose fabricated or impossible statistics.',
        'reading_passage': 'Physical activity has numerous proven benefits. Research has proven that doing ten jumping jacks daily cures depression permanently in 100% of cases. Regular exercise improves sleep.',
        'word_count': 27,
        'article_sentences': [
            {'sentence_id': 's1', 'text': 'Physical activity has numerous proven benefits.', 'is_flawed': False, 'flaw_reason': ''},
            {'sentence_id': 's2', 'text': 'Research has proven that doing ten jumping jacks daily cures depression permanently in 100% of cases.', 'is_flawed': True, 'flaw_reason': 'Jumping jacks curing depression permanently in 100% of cases is wildly inaccurate.'},
            {'sentence_id': 's3', 'text': 'Regular exercise improves sleep.', 'is_flawed': False, 'flaw_reason': ''},
        ],
        'sentence_explanations': {
            's1': 'This is a scientifically backed general statement.',
            's3': 'This is accurate and supported by medical experts.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'One sentence promises a 100% cure rate for depression.'},
            {'tier': 2, 'hint_text': 'Jumping jacks permanently curing depression in all cases is fabricated.'},
            {'tier': 3, 'hint_text': 'Sentence s2 is inaccurate.'},
        ]
    },
    {
        'node_id': 'fac_node_11',
        'title': 'Accuracy Intermediate',
        'focus': 'Identify a moderately inaccurate claim',
        'craap_criterion': 'ACCURACY',
        'micro_lesson_text': 'Intermediate accuracy checks for statistics that contradict well-known biological or demographic facts.',
        'reading_passage': 'Human biology determines left-handedness. Demographic statistics show that ninety-five percent of all humans are born left-handed. Genetic markers indicate hand preferences.',
        'word_count': 22,
        'article_sentences': [
            {'sentence_id': 's1', 'text': 'Human biology determines left-handedness.', 'is_flawed': False, 'flaw_reason': ''},
            {'sentence_id': 's2', 'text': 'Demographic statistics show that ninety-five percent of all humans are born left-handed.', 'is_flawed': True, 'flaw_reason': 'Claiming 95% of humans are left-handed is inaccurate (the actual figure is ~10%).'},
            {'sentence_id': 's3', 'text': 'Genetic markers indicate hand preferences.', 'is_flawed': False, 'flaw_reason': ''},
        ],
        'sentence_explanations': {
            's1': 'This is biologically accurate.',
            's3': 'This aligns with genetic research.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look for an exaggerated statistic about left-handedness.'},
            {'tier': 2, 'hint_text': 'Claiming 95% left-handedness contradicts real statistics.'},
            {'tier': 3, 'hint_text': 'Sentence s2 is inaccurate.'},
        ]
    },
    {
        'node_id': 'fac_node_12',
        'title': 'Accuracy Advanced',
        'focus': 'Detect a subtly fabricated statistic',
        'craap_criterion': 'ACCURACY',
        'micro_lesson_text': 'Advanced accuracy isolates fabricated statistics that sound precise but have zero empirical basis.',
        'reading_passage': 'Cognitive testing tracks academic performance indicators. Research shows that 78.43% of students fail exams if they skip coffee. Study habits predict testing success.',
        'word_count': 24,
        'article_sentences': [
            {'sentence_id': 's1', 'text': 'Cognitive testing tracks academic performance indicators.', 'is_flawed': False, 'flaw_reason': ''},
            {'sentence_id': 's2', 'text': 'Research shows that 78.43% of students fail exams if they skip coffee.', 'is_flawed': True, 'flaw_reason': 'Precisely fabricated statistic linking coffee directly to failing exams is inaccurate.'},
            {'sentence_id': 's3', 'text': 'Study habits predict testing success.', 'is_flawed': False, 'flaw_reason': ''},
        ],
        'sentence_explanations': {
            's1': 'This is a valid scientific observation.',
            's3': 'This is a well-founded correlation in education.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look for an extremely precise statistic about coffee.'},
            {'tier': 2, 'hint_text': 'The claim that 78.43% fail exams without coffee is fabricated.'},
            {'tier': 3, 'hint_text': 'Sentence s2 is inaccurate.'},
        ]
    },
    {
        'node_id': 'fac_node_13',
        'title': 'Purpose Basics',
        'focus': 'Spot overtly biased or insulting language',
        'craap_criterion': 'PURPOSE',
        'micro_lesson_text': 'Purpose checks why info exists. Avoid emotionally charged, manipulative propaganda.',
        'reading_passage': 'Social media connects people. Anyone who uses social media is stupid and destroying their brain. Digital literacy helps users navigate sites.',
        'word_count': 22,
        'article_sentences': [
            {'sentence_id': 's1', 'text': 'Social media connects people.', 'is_flawed': False, 'flaw_reason': ''},
            {'sentence_id': 's2', 'text': 'Anyone who uses social media is stupid and destroying their brain.', 'is_flawed': True, 'flaw_reason': 'Uses insulting ("stupid") and manipulative language, failing Purpose.'},
            {'sentence_id': 's3', 'text': 'Digital literacy helps users navigate sites.', 'is_flawed': False, 'flaw_reason': ''},
        ],
        'sentence_explanations': {
            's1': 'This is a neutral, informative statement.',
            's3': 'This offers constructive advice.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'One sentence insults users directly.'},
            {'tier': 2, 'hint_text': 'Calling users "stupid" violates objective Purpose.'},
            {'tier': 3, 'hint_text': 'Sentence s2 is biased.'},
        ]
    },
    {
        'node_id': 'fac_node_14',
        'title': 'Purpose Intermediate',
        'focus': 'Identify moderately biased framing',
        'craap_criterion': 'PURPOSE',
        'micro_lesson_text': 'Intermediate purpose spots one-sided arguments that completely omit opposing perspectives.',
        'reading_passage': 'Trade tariffs impact local manufacturing. Foreign producers are greedy thieves who want to destroy our workforce. Economists analyze import tax consequences.',
        'word_count': 22,
        'article_sentences': [
            {'sentence_id': 's1', 'text': 'Trade tariffs impact local manufacturing.', 'is_flawed': False, 'flaw_reason': ''},
            {'sentence_id': 's2', 'text': 'Foreign producers are greedy thieves who want to destroy our workforce.', 'is_flawed': True, 'flaw_reason': 'Foreign producers as "greedy thieves" is hostile, one-sided propaganda.'},
            {'sentence_id': 's3', 'text': 'Economists analyze import tax consequences.', 'is_flawed': False, 'flaw_reason': ''},
        ],
        'sentence_explanations': {
            's1': 'This is a neutral economic statement.',
            's3': 'This is an objective description of economist activity.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look for hostile name-calling about foreign trade.'},
            {'tier': 2, 'hint_text': 'Foreigners are "greedy thieves" is non-objective propaganda.'},
            {'tier': 3, 'hint_text': 'Sentence s2 is biased.'},
        ]
    },
    {
        'node_id': 'fac_node_15',
        'title': 'Purpose Advanced',
        'focus': 'Detect subtly manipulative academic language',
        'craap_criterion': 'PURPOSE',
        'micro_lesson_text': 'Advanced purpose isolates sales pitches or marketing agendas disguised as scientific reporting.',
        'reading_passage': 'Cognitive vitamins support neural speed. Our brand is the only formula that guarantees genius. Nutritionists recommend balanced diets.',
        'word_count': 20,
        'article_sentences': [
            {'sentence_id': 's1', 'text': 'Cognitive vitamins support neural speed.', 'is_flawed': False, 'flaw_reason': ''},
            {'sentence_id': 's2', 'text': 'Our brand is the only formula that guarantees genius.', 'is_flawed': True, 'flaw_reason': 'Commercial marketing claim disguised as science violates Purpose.'},
            {'sentence_id': 's3', 'text': 'Nutritionists recommend balanced diets.', 'is_flawed': False, 'flaw_reason': ''},
        ],
        'sentence_explanations': {
            's1': 'This is a general health description.',
            's3': 'This is standard dietetics advice.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look for a product advertisement disguised as health research.'},
            {'tier': 2, 'hint_text': '"Our brand guarantees genius" is commercial sales talk.'},
            {'tier': 3, 'hint_text': 'Sentence s2 is biased.'},
        ]
    },
    {
        'node_id': 'fac_node_16',
        'title': 'Currency Basics 2',
        'focus': 'Spot an obviously outdated technology guide',
        'craap_criterion': 'CURRENCY',
        'micro_lesson_text': 'Currency checks if instructions are relevant. Avoid guides from decades ago.',
        'reading_passage': 'Modern typing requires keyboard layouts. According to a 1982 typing guide, users must clean their metal typewriters daily. Touch screens have modernized communications.',
        'word_count': 25,
        'article_sentences': [
            {'sentence_id': 's1', 'text': 'Modern typing requires keyboard layouts.', 'is_flawed': False, 'flaw_reason': ''},
            {'sentence_id': 's2', 'text': 'According to a 1982 typing guide, users must clean their metal typewriters daily.', 'is_flawed': True, 'flaw_reason': 'Using a 1982 typewriter guide for modern typing is outdated, violating Currency.'},
            {'sentence_id': 's3', 'text': 'Touch screens have modernized communications.', 'is_flawed': False, 'flaw_reason': ''},
        ],
        'sentence_explanations': {
            's1': 'This remains true of keyboard devices.',
            's3': 'This is accurate regarding recent touch interface growth.',
        },
        'scaffold_hints': [
            {'tier': 1, 'hint_text': 'Look for guidance on typewriters from 1982.'},
            {'tier': 2, 'hint_text': 'A 1982 typing guide for typewriters is obsolete today.'},
            {'tier': 3, 'hint_text': 'Sentence s2 is outdated.'},
        ]
    },
]

for node in FACT_SCANNER_NODES:
    ArticleDocument(**node).save()
    print(f"Seeded: {node['node_id']} — {node['title']}")

print("\nAll nodes seeded successfully!")
