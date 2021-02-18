from github import Github
import os
import pandas as pd
import matplotlib.pyplot as plt

if "REPOSITORY" in os.environ:
    repo_name = os.environ["REPOSITORY"]
else:
    repo_name = os.environ["GITHUB_REPOSITORY"]
github = Github(os.environ["TRAFFIC_ACTION_TOKEN"])
print("Repository name: ", repo_name)
repo = github.get_repo(repo_name)

print(os.environ)

workplace_path = "{}/{}".format(os.environ["GITHUB_WORKSPACE"], "traffic")
if not os.path.exists(workplace_path):
    os.makedirs(workplace_path)
print("Workplace path: ", workplace_path)

views_path = "{}/{}".format(workplace_path, "views.csv")
clones_path = "{}/{}".format(workplace_path, "clones.csv")
plots_path = "{}/{}".format(workplace_path, "plots.png")


def main():

    # Traffic stats
    traffic = repo.get_views_traffic()
    traffic_dict = {}
    for view in traffic['views']:
        traffic_dict[view.timestamp] = {"total_views": view.count, "unique_views": view.uniques}
    
    try:
        old_traffic_data = pd.read_csv(views_path, index_col="_date", parse_dates=["_date"]).to_dict(orient="index")
        updated_dict = {**old_traffic_data, **traffic_dict}
        traffic_frame = pd.DataFrame.from_dict(data=updated_dict, orient="index", columns=["total_views", "unique_views"])
    except:
        traffic_frame = pd.DataFrame.from_dict(data=traffic_dict, orient="index", columns=["total_views", "unique_views"])
    
    traffic_frame.index.name = "_date"
    traffic_frame.to_csv(views_path)
    
    print(f"Got {len(traffic_dict)} new views, {len(old_traffic_data)} old views, for {len(updated_dict)} total\n")


    # Clones stats
    clones = repo.get_clones_traffic()
    clones_dict = {}
    for view in clones['clones']:
        clones_dict[view.timestamp] = {"total_clones": view.count, "unique_clones": view.uniques}

    try:
        old_clone_data = pd.read_csv(clones_path, index_col="_date", parse_dates=["_date"]).to_dict(orient="index")
        updated_clones_dict = {**old_clone_data, **clones_dict}
        clones_frame = pd.DataFrame.from_dict(data=updated_clones_dict, orient="index", columns=["total_clones", "unique_clones"])
    except:
        clones_frame = pd.DataFrame.from_dict(data=clones_dict, orient="index", columns=["total_clones", "unique_clones"])
        
    clones_frame.index.name = "_date"
    clones_frame.to_csv(clones_path)

    # Plots
    fig, axes = plt.subplots(nrows=2)
    fig.tight_layout(h_pad=6)

    # Consider letting users configure plots
    # traffic_weekly = traffic_frame.resample("W", label="left").sum().tail(12)
    # clones_weekly = clones_frame.resample("W", label="left").sum().tail(12)
    if not traffic_frame.empty:
        traffic_frame.tail(30).plot(ax=axes[0])
    if not clones_frame.empty: 
        clones_frame.tail(30).plot(ax=axes[1])
    plt.savefig(plots_path)


if __name__ == "__main__":
    main()
