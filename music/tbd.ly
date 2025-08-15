\version "2.24.4"
% automatically converted by musicxml2ly from tbd.musicxml
\pointAndClickOff

\header {
    title =  TBD
    encodingsoftware =  "MuseScore 4.5.2"
    encodingdate =  "2025-08-12"
    }

#(set-global-staff-size 19.997485714285716)
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
PartPOneVoiceOne =  \relative e {
    \clef "bass" \numericTimeSignature\time 4/4 \key a \major | % 1
    \tempo 4=80 \stemDown e2. \stemDown fis8 [ \stemDown gis8 ] | % 2
    \stemDown a2 r8 \stemDown a8 [ \stemDown b8 \stemDown cis8 ] | % 3
    \stemDown d4 \stemDown cis4 \stemDown b4. \stemDown a8 | % 4
    a1 \bar "|."
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

