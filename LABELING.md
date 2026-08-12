# How to label a song

You don't need to be able to name what the instruments are doing. You need one decision,
repeated: *has the feel just changed, and to what?*

## The three-question test

Run these in order. The first "yes" wins.

**1. Is nobody singing, and a guitar is showing off? → MAMBO**

This is the easiest one, and it's why you should find it first. The mambo is the
instrumental break: the requinto (the twangy lead guitar) takes over, the güira goes
rapid-fire, and the whole thing speeds up in feel. Almost every bachata song has exactly
one, usually somewhere after the second chorus.

**2. Is someone singing, and the song just got bigger? → MAJAO**

This is the chorus, nearly always. The song "opens up" — fuller, more driving, more
insistent. If you find yourself wanting to do something bigger than a basic, that's majao.

**3. Is someone singing, and it's calmer? → DERECHO**

The verses. The story-telling part. Sparser, steadier, grounded. This is home base, and
it's usually where a song starts after the intro.

## The single best tell: the güira

The güira is the scratchy metallic shaker — the "chh-chh-chh" running underneath
everything. Its speed is the giveaway:

| Güira | Rhythm |
|---|---|
| Steady, even, unhurried | Derecho |
| Busier, more insistent | Majao |
| Rapid-fire, almost a buzz | Mambo |

If you can only hear one instrument, make it this one.

## Technique that saves you time

**Listen once without labeling.** Just play the song and notice where it changes. You'll
label far more accurately on the second pass because you'll see the changes coming — and
tapping *as* it happens beats tapping *after* you've noticed.

**Do it in passes.** First pass: mark only the mambo break and the choruses. Save. Then
re-open the map and add the verse boundaries. Partial maps are useful immediately — you
don't have to get a whole song in one go.

**Don't fight a bad mark.** Every mark shows its timestamp, with an ✕ to delete it. Fix
afterwards rather than restarting.

**Marks land 250 ms early on purpose**, to cover your reaction time. Tap when you're sure,
not when you're guessing.

## What a typical map looks like

Most bachata songs run about 4 minutes and land around 6–8 marks:

```
0:00  derecho   intro / verse 1
0:45  majao     chorus 1
1:15  derecho   verse 2
1:50  majao     chorus 2
2:20  mambo     instrumental break
2:50  majao     final chorus
3:30  derecho   outro
```

Your timings will differ — that's the shape, not the answer. If you end up with 3 marks or
15, that's fine too; some songs shift constantly and some barely move.

## When you're unsure

Two useful fallbacks:

- **Leave it out.** A gap before your first mark shows as unlabelled on the timeline. An
  honest gap beats a wrong label.
- **Default to derecho.** It's the most common section and the safest guess for anything
  that isn't clearly lifted or clearly instrumental.

## Sharing your maps

Maps live on your device, keyed by Spotify track ID. To ship them to everyone else, hit
**Export all maps** — it copies every map as JSON — and hand that over to be baked into
`BUILTIN_MAPS` in `index.html`. Maps that ship with the app are overridden by a user's own
edits, so nobody gets locked into your labelling.

One caveat: track IDs vary by market, so a map made on one account may not match the same
song elsewhere. If that becomes a real problem, the maps can be keyed by artist and title
instead and resolved against the local catalog.
