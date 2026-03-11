# RESPONSE-CODEX-CAMPAIGN-09-LANE-06-YOUTUBE-BRIDGE-AND-ACUMEN-INGEST-INTEGRATION

**status**: `complete`

## Minimal lawful integration

The narrowest safe seam is an opt-in handoff from `operators/exocortex/youtube_feed_bridge.py` into **Acumen-owned runtime intake artifacts**, not a second bridge-owned queue.

That keeps sovereignty aligned as follows:

1. exocortex remains responsible for capture and event projection
2. Acumen remains responsible for deciding whether a captured YouTube item is admissible into its intake plane
3. the Acumen registry remains the gate; channels absent from the registry are skipped
4. Acumen writes the handoff artifacts under `runtime/acumen/intake/`, and only renders a triage packet when the metadata is complete enough

## Surfaces updated

1. `operators/acumen/build_triage_packet.py`
   - extracted shared video-metadata normalization and validation
   - extracted triage packet rendering into a reusable function
   - added `materialize_youtube_bridge_handoff(...)` so Acumen defines the bridge handoff shape itself
2. `operators/exocortex/youtube_feed_bridge.py`
   - added `--acumen-registry`
   - added `--acumen-runtime-root`
   - after exocortex event emission, optionally calls the Acumen helper to materialize intake artifacts
3. `operators/acumen/README.md`
   - documented the bridge handoff path and the registry gate
4. `runtime/acumen/README.md`
   - made the new Acumen intake artifact locations explicit

## Duplication reduced

Before this change, the bridge could only emit exocortex checkpoints while Acumen had a separate manual video-metadata path for triage packet creation.

After this change:

1. Acumen owns one reusable YouTube video metadata contract
2. direct Acumen triage-packet generation and exocortex bridge handoff both use that same contract
3. the bridge does not invent or own a parallel Acumen queue format

## Verification

Executed:

1. `python3 -m py_compile operators/acumen/build_triage_packet.py operators/exocortex/youtube_feed_bridge.py`
2. `python3 operators/acumen/build_triage_packet.py --registry runtime/acumen/registry.json --channel-id UC_x5XG1OV2P6uZZ5FSM9Ttw --video runtime/acumen/sample-video.json --output /tmp/acumen-triage-packet-test.md`
3. direct helper smoke with a registry-owned channel payload
   - result: `ready_for_triage`
   - outputs created under `/tmp/acumen-bridge-handoff/intake/`
4. sovereignty smoke with an unknown channel payload
   - result: `skipped`
   - no intake files created
5. `python3 operators/exocortex/youtube_feed_bridge.py --help | rg 'acumen-registry|acumen-runtime-root'`

I did **not** run the full bridge end-to-end against the live repo runtime because its existing reconcile step writes tracked repo state under `memory/` and `orchestration/state/`. The new seam itself was verified without mutating those tracked artifacts.

## Diff hygiene

`git diff --check` was run after the edits and returned clean.
