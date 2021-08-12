#!/usb/bin/python3

import mos.helper as helper

import os
import requests
import re
import sys
import string


class TargetGet:
	def __init__(self, target_distro):
		self.target_distro = target_distro

		h = helper.Helper()
		self.mos_path = h.mos_path
		self.arch = h.arch

		self.target_bootstrap_dir = self.mos_path + "/data/build/bootstrap"
		self.distro_rootfs_targz = "rootfs" + "_" + self.target_distro + "_" + self.arch + ".tar.gz"


	def get_alpine(self):

		alpine_mirror = "http://dl-cdn.alpinelinux.org/alpine/"
		alpine_mirror_releases_url = alpine_mirror + "latest-stable/releases/" + self.arch
		alpine_mirror_release = alpine_mirror + "/latest-stable/releases/" + self.arch + "/latest-releases.yaml"
		
		if not os.path.isdir(self.target_bootstrap_dir):
			os.makedirs(self.target_bootstrap_base_dir)
			os.makedirs(self.target_bootstrap_dir)
		else:
			None

		os.chdir(self.target_bootstrap_dir)

		alpine_latest_release = requests.get(alpine_mirror_release, allow_redirects=True)
		open("latest-releases.yaml", 'wb').write(alpine_latest_release.content)

		with open("latest-releases.yaml", "r") as file:
			for line in file:
				if re.search("file: alpine-minirootfs-.*.tar.gz", line):
					target_rootfs_id_full = str(line)
					target_rootfs_id_split = target_rootfs_id_full.split()
					target_rootfs_id = target_rootfs_id_split[1]
					print(target_rootfs_id)

		target_rootfs_url = alpine_mirror_releases_url + "/" + target_rootfs_id
		print(target_rootfs_url)
		target_rootfs_url_request = requests.get(target_rootfs_url, allow_redirects=True)
		open(self.distro_rootfs_targz, 'wb').write(target_rootfs_url_request.content)


	def get_rootfs(self):
		b = TargetGet(self.target_distro)
		if self.target_distro == "alpine":
			b.get_alpine()
		else:
			pass