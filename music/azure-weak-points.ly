\version "2.24.4"
% automatically converted by musicxml2ly from azure-weak-points.musicxml
\pointAndClickOff

\header {
    title =  "Azure Weak Points"
    encodingsoftware =  "MuseScore 4.5.2"
    encodingdate =  "2025-08-11"
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
    short-indent = 1.292923076923077\cm
    }
\layout {
    \context { \Score
        autoBeaming = ##f
        }
    }
PartPOneVoiceOne =  \relative a {
    \repeat volta 16 {
        \clef "bass" \numericTimeSignature\time 4/4 \key a \major | % 1
        \tempo 4=30 \stemDown a4 \stemDown b4 \stemDown cis4 \stemDown d4
        }
    }


% The score definition
\score {
    <<
        
        \new Staff
        <<
            \set Staff.instrumentName = "Piano"
            \set Staff.shortInstrumentName = "Pno."
            
            \context Staff << 
                \mergeDifferentlyDottedOn\mergeDifferentlyHeadedOn
                \context Voice = "PartPOneVoiceOne" {  \PartPOneVoiceOne }
                >>
            >>
        
        >>
    \layout {}
    % To create MIDI output, uncomment the following line:
    %  \midi {\tempo 4 = 30 }
    }

