imprint
=======

This program is a system for data aggregation and presentation through Microsoft
Word documents. It uses templates to define dynamically generated portions of
the document, which the user can construct in arbitrary ways. The content of the
document is separated from the style information and the content generation.

Using this system does not remove the need to write the initial draft of the
document you want to create, or the need to generate the data you plan on
aggregating. This program is only useful if you plan on generating a similarly
formatted document many times with the same content but different data sources.
It is not useful for one-off reports or documents.

See the documentation at <https://imprint.readthedocs.io/en/latest> for more
information, including the history of the project, turorials, and API
references and installation instructions.

The source and binaries for this program are available on PyPI. The simplest
installation method is with `pip`:

    pip install imprint[all]

The extra `[all]` is recommended for but not required. Installing from source
is also an option, by running

    python setup.py install

in the root folder of the project source distribution. The source distribution,
including documentation can be found at <https://github.com/madphysicist/imprint>.

This program in licensed under the AGPLv3 or later. You should have received a
copy of the GNU Affero General Public License along with this program. If not,
see <https://www.gnu.org/licenses/>.
