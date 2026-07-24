# export_core_subjects.py

import os
import json
import importlib.util

SOURCE_FOLDER = "core_subjects"
OUTPUT_FOLDER = "mobile_core_subjects_json"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

exported = 0

for root, dirs, files in os.walk(SOURCE_FOLDER):

    for file in files:

        if not file.endswith(".py"):
            continue

        filepath = os.path.join(root, file)

        try:

            spec = importlib.util.spec_from_file_location(
                "module",
                filepath
            )

            module = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(module)

            if hasattr(module, "TOPICS"):

                output_name = file.replace(
                    ".py",
                    ".json"
                )

                output_path = os.path.join(
                    OUTPUT_FOLDER,
                    output_name
                )

                with open(
                    output_path,
                    "w",
                    encoding="utf-8"
                ) as f:

                    json.dump(
                        module.TOPICS,
                        f,
                        indent=4,
                        ensure_ascii=False
                    )

                exported += 1

                print(
                    f"✅ Exported: {output_name}"
                )

        except Exception as e:

            print(
                f"❌ Failed: {file}"
            )

            print(e)

print(f"\n🎉 Total Files Exported: {exported}")