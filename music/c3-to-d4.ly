\version "2.24.4"
% automatically converted by musicxml2ly from c3-to-d4.musicxml
\pointAndClickOff

\header {
    title =  "c3 to d4"
    encodingsoftware =  "MuseScore 4.5.2"
    encodingdate =  "2025-08-14"
    }

#(set-global-staff-size 19.997457142857144)
\paper {
    
    paper-width = 21.01\cm
    paper-height = 29.69\cm
    top-margin = 1.5\cm
    bottom-margin = 1.5\cm
    left-margin = 1.5\cm
    right-margin = 1.5\cm
    indent = 1.6161538461538463\cm
    short-indent = 0.6464615384615385\cm
    }
\layout {
    \context { \Score
        autoBeaming = ##f
        }
    }
PartPOneVoiceOne =  \relative c {
    \repeat volta 2 {
        \clef "bass" \numericTimeSignature\time 4/4 \key c \major | % 1
        \tempo 4=80 \stemUp c4 \stemDown d4 \stemUp c4 r4 | % 2
        \stemDown d4 \stemDown e4 \stemDown d4 r4 | % 3
        \stemDown e4 \stemDown f4 \stemDown e4 r4 | % 4
        \stemDown f4 \stemDown g4 \stemDown f4 r4 \break | % 5
        \stemDown g4 \stemDown a4 \stemDown g4 r4 | % 6
        \stemDown a4 \stemDown b4 \stemDown a4 r4 | % 7
        \stemDown b4 \stemDown c4 \stemDown b4 r4 | % 8
        \stemDown c4 \stemDown d4 \stemDown c4 r4 \break | % 9
        \stemDown d4 \stemDown c4 \stemDown d4 r4 | \barNumberCheck #10
        \stemDown c4 \stemDown b4 \stemDown c4 r4 | % 11
        \stemDown b4 \stemDown a4 \stemDown b4 r4 | % 12
        \stemDown a4 \stemDown g4 \stemDown a4 r4 \break | % 13
        \stemDown g4 \stemDown f4 \stemDown g4 r4 | % 14
        \stemDown f4 \stemDown e4 \stemDown f4 r4 | % 15
        \stemDown e4 \stemDown d4 \stemDown e4 r4 | % 16
        \stemDown d4 \stemUp c4 \stemDown d4 r4 }
    }


% The score definition
\score {
    <<
        
        \new Staff
        <<
            \set Staff.instrumentName = "Tenor"
            \set Staff.shortInstrumentName = "T."
            
            \context Staff << 
                \mergeDifferentlyDottedOn\mergeDifferentlyHeadedOn
                \context Voice = "PartPOneVoiceOne" {  \PartPOneVoiceOne }
                >>
            >>
        
        >>
    \layout {}
    % To create MIDI output, uncomment the following line:
    %  \midi {\tempo 4 = 80 }
    }

