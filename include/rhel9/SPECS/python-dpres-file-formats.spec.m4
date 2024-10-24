# vim:ft=spec

%define file_prefix M4_FILE_PREFIX
%define file_ext M4_FILE_EXT

%define file_version M4_FILE_VERSION
%define file_release_tag %{nil}M4_FILE_RELEASE_TAG
%define file_release_number M4_FILE_RELEASE_NUMBER
%define file_build_number M4_FILE_BUILD_NUMBER
%define file_commit_ref M4_FILE_COMMIT_REF

Name:           python-dpres-file-formats
Version:        %{file_version}
Release:        %{file_release_number}%{file_release_tag}.%{file_build_number}.git%{file_commit_ref}%{?dist}
Summary:        Machine-readable file formats supported in the DPS
License:        LGPLv3+
URL:            https://www.digitalpreservation.fi
Source0:        %{file_prefix}-v%{file_version}%{?file_release_tag}-%{file_build_number}-g%{file_commit_ref}.%{file_ext}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  %{py3_dist pip}
BuildRequires:  %{py3_dist setuptools}
BuildRequires:  %{py3_dist wheel}
BuildRequires:  %{py3_dist pytest}

%global _description %{expand:
Machine-readable file formats supported in the DPS and python functions to export the data
}

%description %_description

%package -n python3-dpres-file-formats
Summary: %{summary}
%description -n python3-dpres-file-formats %_description

%prep
%autosetup -n %{file_prefix}-v%{file_version}%{?file_release_tag}-%{file_build_number}-g%{file_commit_ref}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files dpres_file_formats

make install-json SHAREDIR=%{buildroot}/usr/share/dpres-file-formats

%files -n python3-dpres-file-formats -f %{pyproject_files}
%doc README.rst
/usr/share/dpres-file-formats/file_formats.json

%changelog
