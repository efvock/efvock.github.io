\version "2.24.2"

\header {
  title = "ピアノ譜"
  composer = "Unknown"
}

upper = \relative c' {
  \clef treble
  \key c \major
  \time 4/4
  c2. c8 b |  % 1
  a4 f b g |  % 2
  c4 g e d |  % 3
  c2. des8 bes |  % 4
  a4 f b g |  % 5
  c4 g e d  % 6
}

lower = \relative c {
  \clef bass
  \key c \major
  \time 4/4
  <c e g>1 |  % C major chord
  <f a c>1 |  % F major chord
  <g b d>1 |  % G major chord
  <c ees aes>1 |  % Cm7 chord
  <f a c>1 |  % F major chord
  <g b d>1  % G major chord
}

\score {
  \new PianoStaff <<
    \new Staff = "upper" \upper
    \new Staff = "lower" \lower
  >>
}
